📊 The MCP Hedge Fund Agent
A collaborative effort to build a sophisticated Model Context Protocol (MCP) ecosystem. Our team developed this lightweight local server/client architecture to demonstrate how Agentic AI can handle complex financial request/response handling and machine learning workflows.
This README.md is specifically designed for your Quant-Analyst MCP project, following the layout and professional structure of the provided screenshots.

Project structure
server.py — Our core server component that integrates yfinance for real-time market data and scikit-learn for predictive modeling.

client.py — An advanced orchestration client designed to send requests and manage the "Chain-of-Thought" tool-calling loop.

requirements.txt — A centralized manifest of our Python dependencies and project metadata for easy group deployment.

.env — Secure environment variables used by our team to manage sensitive API credentials (not checked into source control).

plots/ — A shared output directory for our auto-generated financial visualizations and trend analysis reports.

Requirements
Python 3.10+ (Our team recommends using a virtual environment).

Setup
1. Create and activate a team virtual environment:
   python -m venv .venv
  .\.venv\Scripts\activate

2. Install our project dependencies:
   pip install -r requirements.txt

3. Configure Team Credentials: Create a .env file in the project root with your individual OpenAI API variables:
   OPENAI_API_KEY="your_key_here"

Running
Start the Stock-Analyst Server:
  python client.py server.py

Notes
Data Sources: We standardized our queries to support international tickers (e.g., .NS for NSE India) to ensure global financial coverage.
Security Protocols: To maintain code integrity, keep sensitive values out of source control; use .env and ensure it is listed in .gitignore.

Contributing
Group contributions are welcome — open an issue or PR if you'd like to help us add more financial indicators or sentiment analysis features.
