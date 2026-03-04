# Product Roadmap: Educational DCF Visualizer

## Section 1: The Logic Core (No UI)
Build the pure Python `DCFModel` class.
- Handle 2-stage DCF (projection period + terminal value).
- Inputs: Free Cash Flow (FCF), Growth Rate, WACC, Terminal Growth, Shares Outstanding.
- Output: Enterprise Value, Equity Value, Price per Share.
- **Goal:** Verify the math acts exactly like a textbook example.

## Section 2: The Interactive Shell
Create the basic Streamlit interface.
- Sidebar for inputs (Growth Rate, WACC, etc.).
- Main area displaying the big "Intrinsic Value per Share" number.
- Simple "Cash Flow Projection" table showing the next 5-10 years.
- **Goal:** User can slide a slider and see the numbers move.

## Section 3: The Sensitivity Visualizer
Implement the visual learning layer.
- **Sensitivity Matrix:** A heatmap showing Stock Price at different WACC vs. Growth combinations.
- **Bar Chart:** Visualizing the component value (PV of Stage 1 vs. PV of Terminal Value).
- **Goal:** "Aha!" moment seeing how much value comes from the Terminal Value.

## Section 4: Real-World Data (Optional/Bonus)
Connect `yfinance` to pre-fill inputs.
- "Load Ticker" button.
- Fetches recent FCF and Shares Outstanding.
- **Goal:** Apply the theory to real stocks (AAPL, MSFT).
