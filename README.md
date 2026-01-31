# 📊 MCP Hedge Fund Agent

A collaborative effort to build a **Model Context Protocol (MCP)** ecosystem for financial intelligence.  
This project demonstrates how **Agentic AI** can orchestrate complex **financial data pipelines**, **machine learning workflows**, and **tool-based reasoning** using a lightweight local server–client architecture.

The system is designed for **quantitative analysis**, **market data retrieval**, and **predictive modeling**, making it suitable for research, experimentation, and educational use.

---

## 🧠 Project Overview

The MCP Hedge Fund Agent simulates a modular hedge-fund-style AI analyst by:

- Fetching real-time and historical market data
- Performing statistical and ML-based analysis
- Generating visual insights
- Coordinating reasoning through an agent-style request/response loop

---

## 🗂️ Project Structure

```text
├── server.py
│   └── Core MCP server integrating market data and ML models
│
├── client.py
│   └── Orchestration client managing agent requests and tool-calling flow
│
├── requirements.txt
│   └── Centralized dependency list for reproducible setups
│
├── .env
│   └── Environment variables for sensitive credentials (not committed)
│
├── plots/
│   └── Auto-generated financial charts and analysis reports
│
└── README.

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
