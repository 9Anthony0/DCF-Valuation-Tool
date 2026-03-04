import streamlit as st
import pandas as pd
import yfinance as yf
from dcf_model import DCFModel

def get_company_data(ticker):
    """Fetches financial data and calculates recommendations."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # --- 1. Basic Inputs ---
        shares = info.get('sharesOutstanding', 0) / 1_000_000
        
        # FCF Logic
        cashflow = stock.cashflow
        fcf = 100.0 # fallback
        if cashflow is not None and not cashflow.empty:
            if 'Free Cash Flow' in cashflow.index:
                 fcf = cashflow.loc['Free Cash Flow'].iloc[0] / 1_000_000
            elif 'Operating Cash Flow' in cashflow.index and 'Capital Expenditures' in cashflow.index:
                ocf = cashflow.loc['Operating Cash Flow'].iloc[0]
                capex = cashflow.loc['Capital Expenditures'].iloc[0]
                fcf = (ocf + capex) / 1_000_000
            elif 'Total Cash From Operating Activities' in cashflow.index:
                 ocf = cashflow.loc['Total Cash From Operating Activities'].iloc[0]
                 capex = cashflow.loc['Capital Expenditures'].iloc[0] if 'Capital Expenditures' in cashflow.index else 0
                 fcf = (ocf + capex) / 1_000_000

        # --- 2. Smart WACC (CAPM) ---
        # Formula: Rf + Beta * ERP(5%)
        beta = info.get('beta', 1.0)
        
        # Fetch Risk Free Rate (10Y Treasury)
        rf_rate = 4.0 # Fallback 4%
        try:
            tnx = yf.Ticker("^TNX")
            hist = tnx.history(period="1d")
            if not hist.empty:
                rf_rate = hist['Close'].iloc[-1]
        except:
            pass
            
        rec_wacc = rf_rate + (beta * 5.0)
        wacc_justification = f"Risk-Free {rf_rate:.1f}% + (Beta {beta:.2f} × 5% ERP)"

        # --- 3. Smart Growth (Revenue CAGR) ---
        rec_growth = 10.0 # Fallback
        growth_source = "Assumption"
        try:
            inc = stock.income_stmt
            if inc is not None and not inc.empty and 'Total Revenue' in inc.index:
                revs = inc.loc['Total Revenue'].iloc[:4] # Latest 4 years
                if len(revs) >= 4:
                    # CAGR formula: (End/Start)^(1/n) - 1
                    start_rev = revs.iloc[-1] # Oldest
                    end_rev = revs.iloc[0]    # Newest
                    years = len(revs) - 1
                    if start_rev > 0:
                        cagr = (end_rev / start_rev) ** (1/years) - 1
                        rec_growth = cagr * 100
                        growth_source = f"{years}-Year Revenue CAGR"
        except:
            pass
            
        # --- 4. Balance Sheet & Pricing ---
        total_cash = info.get('totalCash', 0) / 1_000_000
        total_debt = info.get('totalDebt', 0) / 1_000_000
        current_price = info.get('currentPrice', info.get('previousClose', 0.0))

        return {
            'fcf': round(fcf, 2), 
            'shares': round(shares, 2),
            'wacc': round(rec_wacc, 1),
            'growth': round(rec_growth, 1),
            'total_cash': round(total_cash, 2),
            'total_debt': round(total_debt, 2),
            'current_price': current_price,
            'wacc_note': wacc_justification,
            'growth_note': growth_source
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def render_scenario_inputs(key_suffix, defaults):
    """Helper to render inputs for a specific scenario tab."""
    current_fcf = st.number_input(f"Current FCF ($) - {key_suffix}", value=defaults['fcf'], step=10.0, key=f"fcf_{key_suffix}")
    shares = st.number_input(f"Shares (M) - {key_suffix}", value=defaults['shares'], step=1.0, key=f"shares_{key_suffix}")
    
    st.markdown("---")
    growth_rate = st.slider(f"Growth Rate (%) - {key_suffix}", 0.0, 30.0, defaults['growth'], key=f"growth_{key_suffix}") / 100.0
    wacc = st.slider(f"WACC (%) - {key_suffix}", 5.0, 20.0, defaults['wacc'], key=f"wacc_{key_suffix}") / 100.0
    terminal_growth = st.slider(f"Term. Growth (%) - {key_suffix}", 0.0, 5.0, defaults['term'], key=f"term_{key_suffix}") / 100.0
    
    return current_fcf, shares, growth_rate, wacc, terminal_growth

def main():
    st.set_page_config(page_title="DCF Scenarios", layout="wide")
    
    st.title("🐂🐻 DCF Scenario Manager")
    st.markdown("Compare **Base**, **Bull**, and **Bear** cases to understand valuation ranges.")
    
    # --- Sidebar: Real Data ---
    st.sidebar.header("Data Source")
    ticker = st.sidebar.text_input("Load Ticker (e.g. AAPL, MSFT)", value="").upper()
    if st.sidebar.button("Load Data"):
        if ticker:
            with st.spinner(f"Fetching {ticker}..."):
                data = get_company_data(ticker)
                if data:
                    # Store justifications inside session state
                    st.session_state['wacc_note'] = data['wacc_note']
                    st.session_state['growth_note'] = data['growth_note']
                    st.session_state['total_cash'] = data['total_cash']
                    st.session_state['total_debt'] = data['total_debt']
                    st.session_state['current_price'] = data['current_price']

                    # Update widget state for all scenarios so the UI reflects the new company
                    for suffix in ['base', 'bull', 'bear']:
                        st.session_state[f'fcf_{suffix}'] = data['fcf']
                        st.session_state[f'shares_{suffix}'] = data['shares']
                        st.session_state[f'wacc_{suffix}'] = data['wacc']
                        st.session_state[f'growth_{suffix}'] = max(0.0, data['growth']) 
                    
                    st.success(f"Loaded {ticker}!")

    # --- Sidebar Tabs ---
    st.sidebar.header("Scenario Assumptions")
    
    # Show Justifications if available
    if 'wacc_note' in st.session_state:
        st.sidebar.info(f"💡 **Recommendation Logic**\n\n**WACC**: {st.session_state['wacc_note']}\n\n**Growth**: {st.session_state['growth_note']}")

    tab_base, tab_bull, tab_bear = st.sidebar.tabs(["Base", "Bull", "Bear"])
    
    with tab_base:
        st.subheader("Base Case")
        # proper defaults based on loaded data or standard fallback
        def_fcf = st.session_state.get('base_fcf', 100.0)
        def_shares = st.session_state.get('base_shares', 50.0)
        base_inputs = render_scenario_inputs("base", {'fcf': def_fcf, 'shares': def_shares, 'growth': 10.0, 'wacc': 10.0, 'term': 3.0})
        
    with tab_bull:
        st.subheader("Bull Case (Optimistic)")
        bull_inputs = render_scenario_inputs("bull", {'fcf': 120.0, 'shares': 50.0, 'growth': 15.0, 'wacc': 9.0, 'term': 4.0})

    with tab_bear:
        st.subheader("Bear Case (Pessimistic)")
        bear_inputs = render_scenario_inputs("bear", {'fcf': 80.0, 'shares': 50.0, 'growth': 5.0, 'wacc': 12.0, 'term': 2.0})

    # --- Calculations ---
    scenarios = {
        "Base": base_inputs,
        "Bull": bull_inputs,
        "Bear": bear_inputs
    }
    
    results = {}
    
    for name, inputs in scenarios.items():
        # Unpack inputs
        fcf, shares, g, w, term_g = inputs
        
        cash = st.session_state.get('total_cash', 0.0)
        debt = st.session_state.get('total_debt', 0.0)
        
        # Validation
        if w <= term_g:
            st.error(f"⚠️ {name} Case Error: WACC must be > Terminal Growth")
            continue
            
        model = DCFModel(fcf, g, w, term_g, shares, cash, debt)
        results[name] = model.calculate_intrinsic_value()

    # --- Display Detailed Output First ---
    if len(results) == 3:
        st.subheader("Base Case Valuation Breakdown")
        
        current_market = st.session_state.get('current_price', 0.0)
        intrinsic_val = results['Base']['price_per_share']
        
        if current_market > 0:
            diff = intrinsic_val - current_market
            diff_pct = (diff / current_market) * 100
            color = "green" if diff > 0 else "red"
            st.info(f"**Market Context:** The current real-world trading price is **${current_market:.2f}**. Our DCF Intrinsic Value is **${intrinsic_val:.2f}**. A difference exists because the market is pricing in different growth or risk expectations than our Base Case baseline assumptions! Adjust the sliders to see what assumptions justify the current price.")
            
        b1, b2, b3 = st.columns(3)
        b1.metric("Enterprise Value", f"${results['Base']['enterprise_value']:,.2f} M")
        b2.metric("Equity Value (incl. Net Debt)", f"${results['Base']['equity_value']:,.2f} M")
        
        if current_market > 0:
            b3.metric("DCF Intrinsic Value per Share", f"${intrinsic_val:.2f}", f"{diff_pct:.1f}% vs Market")
        else:
            b3.metric("Per-Share Value", f"${intrinsic_val:.2f}")

        st.divider()

        # Metrics Row
        st.subheader("Scenario Comparison")
        c1, c2, c3 = st.columns(3)
        c1.metric("🐻 Bear Value", f"${results['Bear']['price_per_share']:.2f}")
        c2.metric("⚖️ Base Value", f"${results['Base']['price_per_share']:.2f}")
        c3.metric("🐂 Bull Value", f"${results['Bull']['price_per_share']:.2f}")
        
        st.divider()
        
        # Bar Chart Comparison
        st.subheader("Price Comparison")
        comparison_df = pd.DataFrame({
            "Scenario": ["Bear", "Base", "Bull"],
            "Share Price": [results['Bear']['price_per_share'], 
                           results['Base']['price_per_share'], 
                           results['Bull']['price_per_share']]
        })
        st.bar_chart(comparison_df.set_index("Scenario"))
        
        # Detailed Inputs Table
        st.subheader("Input Comparison")
        input_data = {
            "Metric": ["Free Cash Flow", "Growth Rate", "WACC", "Terminal Growth"],
            "Bear 🐻": [f"${bear_inputs[0]:.2f}", f"{bear_inputs[2]:.1%}", f"{bear_inputs[3]:.1%}", f"{bear_inputs[4]:.1%}"],
            "Base ⚖️": [f"${base_inputs[0]:.2f}", f"{base_inputs[2]:.1%}", f"{base_inputs[3]:.1%}", f"{base_inputs[4]:.1%}"],
            "Bull 🐂": [f"${bull_inputs[0]:.2f}", f"{bull_inputs[2]:.1%}", f"{bull_inputs[3]:.1%}", f"{bull_inputs[4]:.1%}"],
        }
        st.dataframe(pd.DataFrame(input_data), use_container_width=True)

        st.divider()

        # Sensitivity Analysis Table
        st.subheader("Sensitivity Analysis (Base Case)")
        st.markdown("Per-Share Value across different WACC and Growth Rate assumptions:")
        
        base_wacc = base_inputs[3]
        base_growth = base_inputs[2]
        
        # 5x5 grid: +/- 1% and +/- 2%
        wacc_range = [base_wacc - 0.02, base_wacc - 0.01, base_wacc, base_wacc + 0.01, base_wacc + 0.02]
        growth_range = [base_growth - 0.02, base_growth - 0.01, base_growth, base_growth + 0.01, base_growth + 0.02]
        
        matrix = []
        for w in wacc_range:
            row = []
            for g in growth_range:
                try:
                    m = DCFModel(base_inputs[0], g, w, base_inputs[4], base_inputs[1])
                    val = m.calculate_intrinsic_value()['price_per_share']
                    row.append(val)
                except ValueError:
                    row.append(None)
            matrix.append(row)
            
        df_sens = pd.DataFrame(matrix, 
                               index=[f"{w*100:.1f}%" for w in wacc_range],
                               columns=[f"{g*100:.1f}%" for g in growth_range])
                               
        st.write("**WACC (Rows) vs. Growth Rate (Columns)**")
        st.dataframe(df_sens.style.background_gradient(cmap='RdYlGn', axis=None).format("${:.2f}", na_rep="N/A"), use_container_width=True)

    else:
        st.warning("Fix errors in scenarios to see comparison.")


if __name__ == "__main__":
    main()
