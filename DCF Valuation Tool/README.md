# Corporate Valuation Application (DCF Model)

## Overview
This is a comprehensive Discounted Cash Flow (DCF) valuation tool built with Python and Streamlit. It calculates the intrinsic value of publicly traded companies by pulling real-time financial data and projecting future cash flows. 

The application goes beyond a rigid single-point estimate by allowing users to instantly compare **Base**, **Bull**, and **Bear** scenarios, and features an interactive sensitivity matrix to visualize how different assumptions impact the final valuation.

## Key Features
- **Live Data Integration:** Automatically fetches current share price, shares outstanding, Free Cash Flow, cash, and debt for any ticker using `yfinance`.
- **Smart Data-Backed Defaults:** 
  - **WACC:** Calculated automatically using the Capital Asset Pricing Model (CAPM) by pulling the current 10-Year Treasury Yield (Risk-Free Rate) and the specific stock's Beta.
  - **Growth Rate:** Pre-populated using the company's actual 3-year historical revenue Compound Annual Growth Rate (CAGR).
- **Scenario Manager:** Side-by-side comparison of Base, Bull (optimistic), and Bear (pessimistic) scenarios with adjustable assumptions for Growth Rate, WACC, and Terminal Growth.
- **Detailed Valuation Output:** Explicit breakdown of Enterprise Value, Equity Value (including Cash and Debt), and intrinsic Per-Share Value.
- **Market Context Analysis:** Computes the percentage difference between the DCF intrinsic value and the actual current market trading price.
- **Sensitivity Matrix:** A 5x5 dynamic table showing how precise changes to WACC and Growth Rate impact the final per-share valuation.

## How to Use the Application

### Prerequisites
Make sure you have Python installed, along with the `uv` package manager (which this project uses for fast dependency resolution). 

### Installation & Running
1. Open your terminal or command prompt.
2. Navigate into this folder (`DCF Valuation Tool`).
3. Run the following command to start the web app:
   ```bash
   uv run streamlit run src/app.py
   ```
4. The application will automatically open in your default web browser (usually at `http://localhost:8501`).

### Step-by-Step Usage
1. **Load a Company:** In the left sidebar, enter a stock ticker (e.g., `AAPL`, `MSFT`, `TSLA`) into the text box and click **Load Data**.
2. **Review the Data:** Wait a few seconds for the app to scrape the financial statements. Read the blue "Recommendation Logic" box to see exactly *why* the app chose its baseline WACC and Growth Rate.
3. **Analyze the Breakdown:** Look at the "Base Case Valuation Breakdown" to see the intrinsic value. Read the green/red market context box to see if the stock is currently undervalued or overvalued compared to its real-world trading price.
4. **Stress Test Assumptions:** In the sidebar, under "Scenario Assumptions", adjust the sliders for the Base, Bull, or Bear cases. 
5. **Compare Scenarios:** Scroll down to the Bar Chart and Input Comparison table to visually compare how your 3 different scenarios stack up against each other.
6. **Sensitivity Matrix:** Scroll to the very bottom to view the 2D Sensitivity Analysis grid. This shows you exactly how much the share price would change if your WACC or Growth assumptions are off by 1% or 2% in either direction.

## Project Structure
- `src/app.py`: The main Streamlit frontend application and `yfinance` data extraction logic.
- `src/dcf_model.py`: The core financial mathematics engine (cash flow projection, terminal value, enterprise/equity value calculation).
- `pyproject.toml` / `uv.lock`: Project dependencies.
- `product/`: Documentation outlining the DRIVER methodology used to develop this application.
- `VIDEO_REQUIREMENTS_GUIDE.md`: A reference script for explaining the model's logic.
