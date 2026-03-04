

class DCFModel:
    def __init__(self, current_fcf, growth_rate, wacc, terminal_growth_rate, shares_outstanding, total_cash=0, total_debt=0, projection_years=5):
        """
        Initialize the DCF Model with core inputs.
        
        Args:
            current_fcf (float): Free Cash Flow for the most recent year.
            growth_rate (float): Expected annual growth rate for the projection period (decimal, e.g. 0.05 for 5%).
            wacc (float): Weighted Average Cost of Capital (decimal).
            terminal_growth_rate (float): Perpetual growth rate after projection period (decimal).
            shares_outstanding (float): Number of shares outstanding.
            total_cash (float): Total cash and equivalents.
            total_debt (float): Total debt.
            projection_years (int): Number of years to project cash flows.
        """
        self.current_fcf = current_fcf
        self.growth_rate = growth_rate
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        self.shares_outstanding = shares_outstanding
        self.total_cash = total_cash
        self.total_debt = total_debt
        self.projection_years = projection_years

    def calculate_projected_cash_flows(self):
        """Generates a list of projected FCFs for the projection years."""
        cash_flows = []
        fcf = self.current_fcf
        for _ in range(self.projection_years):
            fcf *= (1 + self.growth_rate)
            cash_flows.append(fcf)
        return cash_flows

    def calculate_terminal_value(self, last_projected_fcf):
        """Calculates the Terminal Value at the END of the projection period."""
        # Gordon Growth Model: TV = (FCF_n * (1 + g_term)) / (WACC - g_term)
        terminal_cash_flow = last_projected_fcf * (1 + self.terminal_growth_rate)
        
        if self.wacc <= self.terminal_growth_rate:
             raise ValueError("WACC must be greater than Terminal Growth Rate used for Gordon Growth Model.")

        terminal_value = terminal_cash_flow / (self.wacc - self.terminal_growth_rate)
        return terminal_value

    def calculate_intrinsic_value(self):
        """
        Performs the full DCF valuation.
        Returns a dictionary with detailed breakdown.
        """
        projected_fcfs = self.calculate_projected_cash_flows()
        last_fcf = projected_fcfs[-1]
        
        terminal_value = self.calculate_terminal_value(last_fcf)
        
        # Present Value of Projected FCFs
        pv_projected = 0
        for i, fcf in enumerate(projected_fcfs):
            # i+1 because cash flows are at end of year 1, 2, ...
            pv_projected += fcf / ((1 + self.wacc) ** (i + 1))
            
        # Present Value of Terminal Value
        # Discounted back from the end of year N to today
        pv_terminal = terminal_value / ((1 + self.wacc) ** self.projection_years)
        
        total_enterprise_value = pv_projected + pv_terminal
        equity_value = total_enterprise_value + self.total_cash - self.total_debt
        price_per_share = equity_value / self.shares_outstanding if self.shares_outstanding > 0 else 0
        
        return {
            "projected_fcfs": projected_fcfs,
            "terminal_value": terminal_value,
            "pv_projected": pv_projected,
            "pv_terminal": pv_terminal,
            "enterprise_value": total_enterprise_value,
            "equity_value": equity_value,
            "price_per_share": price_per_share
        }
