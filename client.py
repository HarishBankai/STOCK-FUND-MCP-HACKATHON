import asyncio
import sys
import json
import os
import re
import platform
import subprocess
from contextlib import AsyncExitStack
from pathlib import Path
from dotenv import load_dotenv 

# MCP and OpenAI library imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

# Load API keys from .env (OPENAI_API_KEY)
load_dotenv()

OPENAI_MODEL = "gpt-4o-mini" 

class MCPClient:
    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self.openai = AsyncOpenAI()

    async def connect_to_server(self, server_script_path: str):
        """Initializes the connection to the Quant-Analyst MCP server."""
        path = Path(server_script_path).resolve()
        
        # Define how to launch the server
        server_params = StdioServerParameters(
            command="python", 
            args=[str(path)],
            env=None,
        )

        print(f"Connecting to Quant-Analyst server at: {path.name}...")
        
        # Establish the transport and session
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        # Initialize the MCP handshake
        await self.session.initialize()
        
        # Discover available tools
        tools = (await self.session.list_tools()).tools
        print(f"✅ Connected! Tools discovered: {[t.name for t in tools]}")

    def open_visual_report(self, filepath):
        """Cross-platform logic to open generated PNG charts automatically."""
        abs_path = os.path.abspath(filepath)
        try:
            print(f"🖼️ Opening Analyst Report: {filepath}")
            if platform.system() == "Windows":
                os.startfile(abs_path)
            elif platform.system() == "Darwin": # macOS
                subprocess.call(("open", abs_path))
            else: # Linux
                subprocess.call(("xdg-open", abs_path))
        except Exception as e:
            print(f"⚠️ Could not open chart automatically: {e}")

    async def process_query(self, query: str) -> str:
        """The 'Agentic' loop: LLM Reasoning -> Tool Execution -> Result Summary."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a Senior Hedge Fund Analyst. Follow these rules:\n"
                    "1. ANALYZE FIRST: Use 'get_stock_info' for context before 'analyze_stock_trend'.\n"
                    "2. TICKERS: Always append '.NS' for Indian stocks (e.g., RELIANCE.NS).\n"
                    "3. PLOTS: If you mention a chart path (plots/*.png), the client will open it.\n"
                    "4. CALCULATIONS: If the user asks for profit, subtract current from predicted price."
                )
            },
            {"role": "user", "content": query}
        ]

        # Fetch available tools from the server
        mcp_tools = (await self.session.list_tools()).tools
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            } for tool in mcp_tools
        ]

        while True:
            # Call OpenAI with the tool definitions
            response = await self.openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            
            # If no more tool calls are needed, we have the final report
            if not message.tool_calls:
                final_answer = message.content
                
                # Check for a PNG path in the response to trigger the Auto-Open
                chart_match = re.search(r"plots/[\w\.-]+\.png", final_answer)
                if chart_match:
                    self.open_visual_report(chart_match.group(0))
                
                return final_answer

            # Execute the tool calls requested by the LLM
            messages.append(message)
            for call in message.tool_calls:
                tool_name = call.function.name
                tool_args = json.loads(call.function.arguments)
                
                print(f"🛠️ Analyst is running: {tool_name}({tool_args})")
                result = await self.session.call_tool(tool_name, tool_args)
                
                # Feed the data back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result.content)
                })

    async def chat_loop(self):
        """Interactive terminal for the Analyst."""
        print("\n--- Quant-Analyst Terminal Ready ---")
        while True:
            try:
                user_input = input("\nQuery: ").strip()
                if user_input.lower() in ["quit", "exit"]:
                    break
                if not user_input:
                    continue

                answer = await self.process_query(user_input)
                print(f"\n📊 Analyst Response:\n{answer}")
                
            except Exception as e:
                print(f"❌ Analysis Error: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py server.py")
        return

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

