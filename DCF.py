from WACC import WeightedAvgCostCapital

class DCF:
    def __init__(self, 
                 inputs: dict):
        self.inputs = inputs
        self.final_yr = self.inputs['yrs'][-1]
        self.projection_period = len(self.inputs['yrs']) - 1
        self.inputs['wacc'] = WeightedAvgCostCapital(inputs=inputs).wacc

        self.compute_projected_revenue()
        self.compute_ebitda()
        self.compute_depreciation_amortization()
        self.compute_ebit()
        self.compute_unlevered_free_cash_flow()
        self.compute_present_value_ufcf()
        self.compute_exit_multiple_table()

    def compute_projected_revenue(self):
        """
        Computes the Projected Revenue.
        """
        previous_revenue = self.inputs['previous_yr_revenue']
        growth_percent = self.inputs['yr_growth']
        self.projected_revenue = {}
        for key, val in growth_percent.items():
            new_val = round(previous_revenue * (1 + val), 2)
            previous_revenue = new_val
            self.projected_revenue.update({key: new_val})

    def compute_ebitda(self):
        """
        Computes the EBITDA according to EBITDA margins
        and the Projected Revenue.
        """
        self.ebitda = {key: round(val * self.inputs['ebitda_margin'].get(key), 2) for (key, val) in self.projected_revenue.items()}

    def compute_depreciation_amortization(self):
        """
        Compute the D&A according to an assumption 
        and the Projected Revenue.
        """
        self.dna = {key: round(val * self.inputs['dna'].get(key), 2) for (key, val) in self.projected_revenue.items()}

    def compute_ebit(self):
        """
        Compute the Operating Income according to the 
        EBITDA and the EBIT margin.
        """
        self.ebit = {key: round(val - self.dna.get(key), 2) for (key, val) in self.ebitda.items()}

    def compute_projected_taxes(self):
        """
        Compute the Taxes for the projected years
        """
        self.tax = {key: round(val * self.inputs['tax_percent'].get(key), 2) for (key, val) in self.ebit.items()}

    def compute_capex(self):
        """
        Compute the Capital Expenditure
        """
        self.capex = {key: round(val * self.inputs['capex_percent'].get(key), 2) for (key, val) in self.projected_revenue.items()}
    
    def compute_nwc(self):
        """
        Compute Net Working Capital 
        """
        self.net_working_capital = {key: round(val * self.inputs['nwc_percent'].get(key), 2) for (key, val) in self.projected_revenue.items()}
        
    def compute_unlevered_free_cash_flow(self):
        # have to compute capex, changes in net working cap
        """
        Compute the Unlevered Free Cash Flow using 
        EBITDA, Taxes, Capital Expenditure, and 
        Change in Net Working Capital.
        """
        self.compute_projected_taxes()
        self.compute_capex()
        self.compute_nwc()
        self.unlevered_free_cash_flow = {key: round(val - self.tax.get(key) - self.capex.get(key) - self.net_working_capital.get(key), 2) for (key, val) in self.ebitda.items()}

    def compute_discount_factor(self):
        """
        Computes the Discount Factor.
        """
        self.discount_factor = {}
        for i, key in enumerate(self.projected_revenue.keys()): 
            val = (1/(1 + self.inputs['wacc']) ** (i + 1))
            discount_factor = round(val, 2)
            self.discount_factor.update({key: discount_factor})


    def compute_present_value_ufcf(self):
        """
        Computes the Present Value Unlevered 
        Free Cash Flow.
        """
        self.compute_discount_factor()
        self.pv_ufcf = {key: round(val * self.discount_factor.get(key), 2) for (key, val) in self.unlevered_free_cash_flow.items()}

    def compute_terminal_value(self):
        """
        Computes the Terminal Value for
        the Exit Multiple Method.
        """
        self.final_ebitda = self.ebitda[self.final_yr]
        self.terminal_value = round(self.final_ebitda * self.inputs['exit_multiple'], 2)

    def compute_present_terminal_value(self):
        """
        Computes the Present Terminal Value.
        """
        self.pv_tv = round(self.terminal_value / ((1 + self.inputs['wacc']) ** self.projection_period), 2)

    def compute_cumulative_pv_ufcf(self):
        """
        Computes the cumulative present value of 
        the Unlevered Free Cash Flow.
        """
        self.sum_pv_ufcf = round(sum(self.pv_ufcf.values()), 2)

    def compute_implied_enterprise_value(self):
        """
        Computes the Implied Enterprise Value.
        """
        self.compute_present_terminal_value()
        self.compute_cumulative_pv_ufcf()
        self.implied_enterprise_value = round(self.sum_pv_ufcf + self.pv_tv, 2)

    def compute_implied_equity_value(self):
        """
        Computes the Implied Equity Value.
        """
        self.implied_equity_value = round(self.implied_enterprise_value + self.inputs['cash'] - self.inputs['debt'], 2)

    def compute_implied_share_price(self):
        """
        Computes the Implied Share Price.
        """
        self.implied_share_price = round(self.inputs['shares_outstanding'] / self.implied_equity_value, 5)

    def compute_safety_margin(self):
        """
        Computes the Safety Margin of a Company.
        """
        self.safety_margin = 1 - (self.inputs['current_share_price']/self.implied_share_price)

    def compute_exit_multiple_table(self):
        """
        Computes the Exit Multiple Method table.
        """
        self.compute_terminal_value()
        self.compute_present_terminal_value()
        self.compute_implied_enterprise_value()
        self.compute_implied_equity_value()
        self.compute_implied_share_price()
        self.compute_safety_margin()

# Test

"""inputs = {
    'business_risk_analysis': 'low',
    'financial_risk_analysis': 'low',
    'risk_free_rate': 0.02,
    'bond_spread': 0.01,
    'tax_rate': 0.3,
    'equity': 3000,
    'current_share_price': 14, 
    'shares_outstanding': 100, 
    'cash': 500,
    'debt': 25, 
    'wacc': 0.1, 
    'yrs': [2024, 2025, 2026],
    'previous_yr_revenue': 2200,
    'yr_growth': {2024: 0.02, 2025: 0.02, 2026: 0.02}, 
    'ebitda_margin': {2024: 0.05, 2025: 0.05, 2026: 0.05},
    'dna': {2024: 0.034, 2025: 0.034, 2026: 0.034}, 
    'tax_percent': {2024: 0.14, 2025: 0.14, 2026: 0.14},
    'capex_percent': {2024: 0.04, 2025: 0.04, 2026: 0.04},
    'nwc_percent': {2024: 0.01, 2025: 0.01, 2026: 0.01},
    'exit_multiple': 3
}

test = DCF(inputs=inputs)"""

    

