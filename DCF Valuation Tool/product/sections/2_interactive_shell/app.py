import streamlit as st
import pandas as pd
from dcf_model import DCFModel

def main():
    st.set_page_config(page_title="Educational DCF Visualizer", layout="wide")
    
    st.title("🎓 Educational DCF Visualizer")
    st.markdown("""
    > **"Price is what you pay. Value is what you get."** — Warren Buffett
    
    Welcome! This tool helps you understand how **Discounted Cash Flow (DCF)** works.
    Change the inputs on the left and see how they impact the **Intrinsic Value** significantly.
    """)
    
    # --- Sidebar Inputs ---
    st.sidebar.header("DCF Assumptions")
    
    current_fcf = st.sidebar.number_input("Current Free Cash Flow ($)", value=100.0, step=10.0)
    shares = st.sidebar.number_input("Shares Outstanding (Millions)", value=50.0, step=1.0)
    
    st.sidebar.subheader("Growth Stage (Next 5 Years)")
    growth_rate = st.sidebar.slider("Growth Rate (%)", 0.0, 30.0, 10.0) / 100.0
    
    st.sidebar.subheader("Discounting & Terminal Value")
    wacc = st.sidebar.slider("WACC (Discount Rate %)", 5.0, 20.0, 10.0) / 100.0
    terminal_growth = st.sidebar.slider("Terminal Growth Rate (%)", 0.0, 5.0, 3.0) / 100.0
    
    # --- Sanity Check ---
    if wacc <= terminal_growth:
        st.error("⚠️ Error: WACC must be higher than Terminal Growth Rate (otherwise value is infinite).")
        return

    # --- Calculation ---
    model = DCFModel(
        current_fcf=current_fcf,
        growth_rate=growth_rate,
        wacc=wacc,
        terminal_growth_rate=terminal_growth,
        shares_outstanding=shares
    )
    
    results = model.calculate_intrinsic_value()
    
    # --- Results Display ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Intrinsic Value / Share", f"${results['price_per_share']:.2f}")
    
    with col2:
        st.metric("Enterprise Value", f"${results['enterprise_value']:,.0f}")
    
    with col3:
        share_pv_projected = (results['pv_projected'] / results['enterprise_value']) * 100
        share_pv_terminal = (results['pv_terminal'] / results['enterprise_value']) * 100
        st.write(f"**Value Split:**")
        st.caption(f"Next 5 Years: {share_pv_projected:.1f}%")
        st.caption(f"Terminal Value: {share_pv_terminal:.1f}%")

    st.divider()
    
    # --- Detailed Breakdown ---
    st.subheader("📊 Cash Flow Projections")
    
    years = range(1, 6)
    df = pd.DataFrame({
        "Year": years,
        "Projected FCF": results['projected_fcfs']
    })
    
    # Formatting for display
    st.dataframe(df.style.format({"Projected FCF": "${:,.2f}"}), use_container_width=True)
    
    st.info("Notice how the 'Terminal Value' often accounts for the majority of the stock price. This is why small changes in WACC or Terminal Growth can have huge effects!")

if __name__ == "__main__":
    main()
