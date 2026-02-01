import asyncio
import os
import uuid
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from mcp.server.fastmcp import FastMCP

# Use a non-interactive backend for headless/terminal use
matplotlib.use("Agg")
import matplotlib.pyplot as plt

server = FastMCP("QuantAnalyst-Pro")

# Real browser headers to prevent Yahoo Finance from blocking the script
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_backup_price(ticker: str) -> str:
    """Fallback: Gets live price if API historical download fails."""
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # Target the fin-streamer tag (standard in 2026)
        price_tag = soup.find("fin-streamer", {"data-symbol": ticker, "data-field": "regularMarketPrice"})
        return f"Current Price (Live Scraped): ₹{price_tag.text}" if price_tag else "N/A"
    except Exception:
        return "Scraping failed."

@server.tool()
async def analyze_stock_trend(ticker: str, period: str = "1y") -> str:
    try:
        # 1. Download with multi_level_index=False to simplify columns
        # Adding auto_adjust=True helps keep column names consistent
        data = yf.download(ticker, period=period, progress=False, multi_level_index=False, auto_adjust=True)
        
        if data.empty:
            return f"Error: No data found for {ticker}. Check if the ticker symbol is correct."

        # 2. Safety Layer: Flatten columns manually if they are still MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # 3. Clean Gaps: Remove NaN values that crash Scikit-Learn
        data = data.dropna(subset=['Close'])
        
        if len(data) < 10:
            return f"Error: Insufficient data points for {ticker} after cleaning."

        # 4. Regression Logic
        data['Days'] = range(len(data))
        X = data[['Days']].values
        y = data['Close'].values.flatten()

        model = LinearRegression().fit(X, y)

        # 5. Forecast
        future_indices = np.array([[len(data) + i] for i in range(1, 6)])
        preds = model.predict(future_indices)

        # Plotting (keep your existing logic)
        os.makedirs("plots", exist_ok=True)
        filename = f"plots/stock_{ticker}_{uuid.uuid4().hex[:6]}.png"
        
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, y, label="Actual Price", color="blue")
        plt.plot(data.index, model.predict(X), label="Trend Line", linestyle="--", color="orange")
        plt.title(f"{ticker} Forecast Analysis")
        plt.legend(); plt.grid(True, alpha=0.3)
        plt.savefig(filename)
        plt.close()

        pred_str = ", ".join([f"₹{p:.2f}" for p in preds])
        return f"Trend for {ticker} analyzed. Predicted next 5 days: {pred_str}. Chart: {filename}"

    except Exception as e:
        return f"Technical Error analyzing {ticker}: {str(e)}"

@server.tool()
async def get_stock_info(ticker: str) -> str:
    """Fetches key fundamentals for the analyst."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return (f"Stats for {ticker}:\n"
                f"- Market Cap: ₹{info.get('marketCap', 'N/A'):,}\n"
                f"- P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
                f"- Summary: {info.get('longBusinessSummary', 'N/A')[:150]}...")
    except Exception as e:
        return f"Fundamental Error: {str(e)}"

def main():
    server.run(transport="stdio")

if __name__ == "__main__":
    main()

