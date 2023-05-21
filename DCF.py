from WACC import WeightedAvgCostCapital
import pandas as pd

class DCF:
    def __init__(self, 
                 inputs: dict):
        self.inputs = inputs
        self.final_yr = self.inputs['yrs'][-1]
        self.projection_period = len(self.inputs['yrs']) - 1
        self.inputs['wacc'] = WeightedAvgCostCapital(inputs=inputs).wacc

        self.dcf_df = pd.DataFrame(columns=['projected_revenue'])
        self.exit_multiple_method_df = pd.DataFrame(columns=['terminal_value'])

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
        
        """# New
        for key, val in growth_percent.items(): 
            new_val = round(previous_revenue * (1 + val), 2)
            previous_revenue = new_val
            self.df.loc[len(self.df)] = new_val"""

        for i in self.inputs['yrs']:
            new_val = previous_revenue * (1 + growth_percent)
            previous_revenue = new_val
            self.dcf_df.loc[len(self.dcf_df)] = new_val

    def compute_ebitda(self):
        """
        Computes the EBITDA according to EBITDA margins
        and the Projected Revenue.
        """

        self.dcf_df['ebitda'] = self.inputs['ebitda_margin'] * self.dcf_df['projected_revenue']

    def compute_depreciation_amortization(self):
        """
        Compute the D&A according to an assumption 
        and the Projected Revenue.
        """

        self.dcf_df['dna'] = self.inputs['dna'] * self.dcf_df['projected_revenue']

    def compute_ebit(self):
        """
        Compute the Operating Income according to the 
        EBITDA and the EBIT margin.
        """

        self.dcf_df['ebit'] = self.dcf_df['ebitda'] - self.dcf_df['dna']

    def compute_projected_taxes(self):
        """
        Compute the Taxes for the projected years
        """

        self.dcf_df['tax'] = self.dcf_df['ebit'] * self.inputs['tax_percent']


    def compute_capex(self):
        """
        Compute the Capital Expenditure
        """

        self.dcf_df['capex'] = self.dcf_df['projected_revenue'] * self.inputs['capex_percent']
    
    def compute_nwc(self):
        """
        Compute Net Working Capital 
        """

        self.dcf_df['net_working_capital'] = self.dcf_df['projected_revenue'] * self.inputs['nwc_percent']
        
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

        self.dcf_df['unlevered_free_cash_flow'] = self.dcf_df['ebitda'] 
        - self.dcf_df['tax'] 
        - self.dcf_df['capex'] 
        - self.dcf_df['net_working_capital']

    def compute_discount_factor(self):
        """
        Computes the Discount Factor.
        """

        """self.discount_factor = {}
        for i, key in enumerate(self.projected_revenue.keys()): 
            val = (1/(1 + self.inputs['wacc']) ** (i + 1))
            discount_factor = round(val, 2)
            self.discount_factor.update({key: discount_factor})"""

        for idx in self.dcf_df.index: 
            val = (1 / (1 + self.inputs['wacc']) ** (idx + 1))
            self.dcf_df['discount_factor'] = val


    def compute_present_value_ufcf(self):
        """
        Computes the Present Value Unlevered 
        Free Cash Flow.
        """
        self.compute_discount_factor()
        self.dcf_df['pv_ufcf'] = self.dcf_df['unlevered_free_cash_flow'] * self.dcf_df['discount_factor']

    def compute_terminal_value(self):
        """
        Computes the Terminal Value for
        the Exit Multiple Method.
        """
        self.final_ebitda = self.dcf_df['ebitda'].iloc[len(self.dcf_df)-1]
        self.exit_multiple_method_df.loc[len(self.exit_multiple_method_df)] = self.final_ebitda * self.inputs['exit_multiple']

    def compute_present_terminal_value(self):
        """
        Computes the Present Terminal Value.
        """
        self.exit_multiple_method_df['pv_tv'] = self.exit_multiple_method_df['terminal_value'] / ((1 + self.inputs['wacc']) ** self.projection_period)

    def compute_cumulative_pv_ufcf(self):
        """
        Computes the cumulative present value of 
        the Unlevered Free Cash Flow.
        """

        self.exit_multiple_method_df['sum_pv_ufcf'] = self.dcf_df['pv_ufcf'].sum()

    def compute_implied_enterprise_value(self):
        """
        Computes the Implied Enterprise Value.
        """
        self.compute_present_terminal_value()
        self.compute_cumulative_pv_ufcf()

        self.exit_multiple_method_df['implied_enterprise_value'] = self.exit_multiple_method_df['sum_pv_ufcf'] 
        + self.exit_multiple_method_df['pv_tv']

    def compute_implied_equity_value(self):
        """
        Computes the Implied Equity Value.
        """
        self.exit_multiple_method_df['implied_equity_value'] = self.exit_multiple_method_df['implied_enterprise_value'] 
        + self.inputs['cash'] 
        - self.inputs['debt']

    def compute_implied_share_price(self):
        """
        Computes the Implied Share Price.
        """
        self.exit_multiple_method_df['implied_share_price'] = self.inputs['shares_outstanding'] / self.exit_multiple_method_df['implied_equity_value']

    def compute_safety_margin(self):
        """
        Computes the Safety Margin of a Company.
        """
        self.exit_multiple_method_df['safety_margin'] = 1 - (self.inputs['current_share_price']/self.exit_multiple_method_df['implied_share_price'])

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
    'yr_growth': 0.02,
    'ebitda_margin': 0.05,
    'dna': 0.034,
    'tax_percent': 0.14,
    'capex_percent': 0.04,
    'nwc_percent': 0.01,
    'exit_multiple': 3
}

test = DCF(inputs=inputs)
print(test.dcf_df)
print(test.exit_multiple_method_df)"""


    

