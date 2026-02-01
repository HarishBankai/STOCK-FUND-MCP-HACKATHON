import asyncio
import os
import uuid
import math
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("Agg")  # CRITICAL for headless server environments
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from mcp.server.fastmcp import FastMCP

# 1. Initialize Server
server = FastMCP("QuantAnalyst-Calculator")

# --- SECTION 1: FINANCIAL TOOLS (Quant-Analyst) ---

@server.tool()
async def analyze_stock_trend(ticker: str, period: str = "1y") -> str:
    """Fetches stock data and calculates a 5-day predictive trend using Linear Regression."""
    try:
        data = yf.download(ticker, period=period)
        if data.empty:
            return f"Error: No data found for {ticker}"

        # Prepare regression
        data['Days'] = range(len(data))
        X = data[['Days']].values
        y = data['Close'].values

        model = LinearRegression()
        model.fit(X, y)

        # Predict future
        future_indices = np.array([[len(data) + i] for i in range(1, 6)])
        preds = model.predict(future_indices)

        # Plotting logic integrated from your plot_xy_graph style
        os.makedirs("plots", exist_ok=True)
        filename = f"plots/stock_{ticker}_{uuid.uuid4().hex[:6]}.png"

        plt.figure(figsize=(10, 5))
        plt.plot(data.index, y, label="Actual Price")
        plt.plot(data.index, model.predict(X), label="Trend Line", linestyle="--")
        plt.title(f"{ticker} Analysis & 5-Day Forecast")
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        plt.close()

        pred_str = ", ".join([f"${p:.2f}" for p in preds.flatten()])
        return f"Trend for {ticker} analyzed. Predicted next 5 days: {pred_str}. Chart: {filename}"
    except Exception as e:
        return f"Error analyzing {ticker}: {str(e)}"

# --- SECTION 2: CALCULATOR & PLOTTING TOOLS ---

@server.tool()
async def add(a: float, b: float) -> str:
    """Adds two numbers."""
    return str(a + b)

@server.tool()
async def div(a: float, b: float) -> str:
    """Divides two numbers."""
    return str(a / b) if b != 0 else "Error: Division by zero"

@server.tool()
async def plot_square_graph(start: float, end: float) -> str:
    """Plot y = x^2 between two values."""
    x = np.linspace(start, end, 200)
    y = x ** 2
    
    os.makedirs("plots", exist_ok=True)
    filename = f"plots/square_plot_{uuid.uuid4().hex[:6]}.png"
    
    plt.figure()
    plt.plot(x, y)
    plt.title("y = x²")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    return f"Square graph saved at: {filename}"

# --- SECTION 3: RUNNER ---

def main():
    server.run(transport="stdio")

if __name__ == "__main__":
    main() 