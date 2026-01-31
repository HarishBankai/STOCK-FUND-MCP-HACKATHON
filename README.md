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
└── README.md
⚙️ Core Components
server.py
Acts as the MCP-compliant server

Integrates:

yfinance for market data

scikit-learn for predictive modeling

Handles structured financial queries and responses

client.py
Agent orchestration layer

Manages request routing, tool invocation, and reasoning loops

Designed to simulate chain-of-thought style tool usage

📦 Requirements
Python 3.10+

Virtual environment recommended

🚀 Setup Instructions
1️⃣ Create & Activate Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate
(On macOS/Linux)

python3 -m venv .venv
source .venv/bin/activate
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure Environment Variables
Create a .env file in the project root:

OPENAI_API_KEY="your_key_here"
⚠️ Never commit .env files to source control.

▶️ Running the Project
Start the Stock-Analyst MCP Server via the client:

python client.py server.py
This launches the MCP workflow where the client orchestrates analytical requests to the server.

📈 Data Sources & Market Coverage
Powered by Yahoo Finance

Supports international tickers

Example:

AAPL (US)

RELIANCE.NS (India – NSE)

Enables global equity, ETF, and index analysis

📊 Output & Visualizations
All generated charts and analysis reports are saved in:

plots/
Includes trend analysis, forecasts, and statistical summaries

🔐 Security Notes
API keys are managed using environment variables

.env is excluded from version control

Designed for local execution only

🧪 Intended Use Cases
Quantitative finance experiments

Agentic AI research

MCP protocol demonstrations

Educational & academic projects

📄 License
This project is provided for research and educational purposes.
Add a license file if you plan to open-source or distribute commercially.
