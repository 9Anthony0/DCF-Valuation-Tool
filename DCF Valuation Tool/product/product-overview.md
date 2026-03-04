# Educational DCF Visualizer

## The Problem
Students and beginners learn the DCF formula ($PV = \sum \frac{CF}{(1+r)^t}$) but struggle to grasp **sensitivity**. They treat the output as a "fact" rather than an estimate highly dependent on adjacent inputs (WACC, Terminal Growth). existing tools are either "black boxes" or complex Excel sheets.

## Success Looks Like
A "glass box" valuation tool. 
- **Interactive:** Sliders for Growth and WACC.
- **Visual:** Charts showing how Intrinsic Value curves as inputs change.
- **Educational:** Explanations for *why* a change happened (e.g., "Increasing WACC lowers value because future cash is worth less").

## Building On (Existing Foundations)
- **numpy-financial** (or simple `numpy`): For standard NPV calculations.
- **Streamlit:** For the interactive "app" experience without complex frontend code.
- **Damodaran's Teaching:** Focus on the "story" behind the numbers, not just the math.

## The Unique Part
**The "Why" Layer.** Unlike a standard calculator, this app focuses on the *relationship* between variables. It explicitly visualizes the "Sensitivity Matrix" (Growth vs. WACC) which is usually a static table in Excel.

## Tech Stack
- **UI:** Streamlit
- **Backend/Logic:** Pure Python (pandas/numpy)
- **Data:** Manual entry (focus on concepts first) with optional `yfinance` later.
