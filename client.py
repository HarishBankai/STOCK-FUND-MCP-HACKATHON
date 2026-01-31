import asyncio
import sys
import json
from contextlib import AsyncExitStack
from pathlib import Path
from dotenv import load_dotenv 

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

# Load API keys from .env
load_dotenv()

# We use gpt-4o-mini for high speed and low cost during the hackathon
OPENAI_MODEL = "gpt-4o-mini" 

class MCPClient:
    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self.openai = AsyncOpenAI()

    async def connect_to_server(self, server_script_path: str):
        """Standardize the connection to the Quant-Analyst server."""
        path = Path(server_script_path).resolve()
        
        # Use 'python' instead of 'uv' for a more direct connection
        server_params = StdioServerParameters(
            command="python", 
            args=[str(path)],
            env=None,
        )

        print(f"Connecting to Quant-Analyst server at: {path.name}...")
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
        
        # Discover the Quant tools (get_stock_trend, find_similar_stocks)
        tools = (await self.session.list_tools()).tools
        print("\n✅ Connected! Tools discovered:", [t.name for t in tools])

    async def process_query(self, query: str) -> str:
        """Handles the 'Agentic' loop where the LLM can call multiple tools."""
        messages = [{"role": "user", "content": query}]

        # 1. Fetch current tools from your MCP server
        mcp_tools = (await self.session.list_tools()).tools
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in mcp_tools
        ]

        # 2. Start the conversation loop
        while True:
            response = await self.openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            
            # If no tool calls, return the final analyst summary
            if not message.tool_calls:
                return message.content

            # Otherwise, execute the tool calls
            messages.append(message)
            for call in message.tool_calls:
                tool_name = call.function.name
                tool_args = json.loads(call.function.arguments)

                print(f"🛠️ Analyst is running tool: {tool_name}({tool_args})")
                
                # Execute on server
                result = await self.session.call_tool(tool_name, tool_args)
                
                # Format result back to OpenAI
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result.content)
                })
                
            # The loop continues to see if the LLM needs more tools (like plotting after analysis)

    async def chat_loop(self):
        print("\n--- Quant-Analyst Terminal Ready ---")
        print("Type 'quit' to exit.")

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
                print(f"❌ Error during analysis: {e}")

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