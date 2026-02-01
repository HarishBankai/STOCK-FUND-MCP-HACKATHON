# 📊 Quant-Analyst MCP

A collaborative quantitative finance project built on the **Model Context Protocol (MCP)**. This repository demonstrates how **Agentic AI systems** can orchestrate real-time financial data retrieval, machine‑learning workflows, and structured tool‑calling using a lightweight local **server–client architecture**.

Designed for **research, experimentation, and team-based development**.

---

## 🚀 Key Features

* 📈 Real-time & historical market data via **Yahoo Finance**
* 🤖 Agentic request/response handling using **MCP**
* 🧠 Machine‑learning models for predictive analysis
* 🔁 Client‑driven tool orchestration loop
* 📊 Auto‑generated plots and trend analysis
* 🌍 Global ticker support (NYSE, NASDAQ, NSE, etc.)

---

## 🗂️ Project Structure

```text
quant-analyst/
│
├── server.py        # MCP server: market data ingestion + ML models
├── client.py        # Agentic client orchestrating tool calls
├── requirements.txt # Python dependencies
├── .env             # Environment variables (not committed)
├── plots/           # Generated charts and analysis outputs
└── README.md
```

### File Overview

* **`server.py`**
  Implements the MCP server and exposes tools for:

  * Fetching financial data using `yfinance`
  * Running predictive models with `scikit-learn`

* **`client.py`**
  Acts as the orchestration layer, managing:

  * Tool invocation
  * Request routing
  * Structured responses from the MCP server

* **`plots/`**
  Output directory for generated visualizations and reports.

---

## ⚙️ Requirements

* **Python 3.10+**
* Recommended: Python virtual environment (`venv`)

---

## 🛠️ Setup

### 1️⃣ Create & Activate a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---

### 2️⃣ Install MCP CLI & Core Utilities

```powershell
uv add mcp[cli] httpx use
```

---

### 3️⃣ Update `pip`

```powershell
python -m ensurepip --upgrade
pip install --upgrade pip
```

---

### 4️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 5️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```plaintext
OPENAI_API_KEY=your_api_key_here
```

> 🔐 **Security Note**
> Ensure `.env` is included in `.gitignore` to prevent accidental commits of sensitive credentials.

---

## ▶️ Running the Project

Start the Quant‑Analyst MCP server via the client:

```powershell
python client.py server.py
```

This launches:

* The MCP server exposing financial analysis tools
* The client orchestration loop handling agentic workflows

---

## 🌍 Market Coverage

The system supports **international tickers** following Yahoo Finance conventions:

* `AAPL` – Apple (US)
* `TSLA` – Tesla (US)
* `RELIANCE.NS` – Reliance Industries (India – NSE)
* `INFY.NS` – Infosys (India – NSE)

---

## 🔐 Security Best Practices

* Never commit API keys or secrets
* Always use `.env` for sensitive configuration
* Rotate API keys periodically
* Review generated outputs before sharing

---

## 🤝 Contributing

Contributions are welcome!

You can help by:

* Adding technical indicators (RSI, MACD, Bollinger Bands)
* Improving ML models
* Integrating sentiment or news analysis
* Enhancing MCP tool workflows

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

---

## 🛣️ Roadmap

* [ ] Expanded technical indicators
* [ ] News & sentiment analysis
* [ ] Backtesting framework
* [ ] Multi‑asset portfolio modeling
* [ ] Interactive dashboard

---

## 📄 License

This project is intended for **educational and research purposes**.
Add a license file if you plan public or commercial distribution.

---

Author : Team Brokers (Harish Ambalgikar, Vaishnavi Patane, Aniket Bade)
