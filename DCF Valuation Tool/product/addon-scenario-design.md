# Add-on: Scenario Manager

## Concept
Allow users to define **Bull**, **Base**, and **Bear** cases to see how valuation ranges.

## User Interface
### Sidebar
Transform the simpler sidebar into **Tabs**:
1.  **Base Case** (Default)
2.  **Bull Case** (Optimistic)
3.  **Bear Case** (Pessimistic)

Each tab contains the same 4 sliders/inputs:
-   Current FCF
-   Shares
-   Growth Rate
-   WACC
-   Terminal Growth

### Main Area
-   **Comparison Metrics:** Display Intrinsic Value per Share for all 3 scenarios side-by-side.
-   **Visuals:**
    -   Bar chart comparing the 3 Share Prices.
    -   Detailed table showing the inputs for each scenario to compare assumptions.

## Technical Implementation
-   Use `st.sidebar.tabs(["Base", "Bull", "Bear"])`.
-   Use unique keys for widgets (e.g., `wacc_base`, `wacc_bull`).
-   Calculate 3 distinct `DCFModel` instances.
-   Combine results into a comparison DataFrame.
