class WeightedAvgCostCapital: 
    # Dictionaries of Equity Risk Premiums

    def __init__(self,
                 inputs: dict) -> float:
        """
        Establish the ERP of a Company 
        using a Weighted Average Cost of Capital (WACC) table.
        """

        self.equity = inputs['equity']
        self.debt = inputs['debt']
        self.total_value = self.equity + self.debt

        self.percent_equity = self.equity / self.total_value
        self.percent_debt = self.debt / self.total_value

        self.business_risk = inputs['business_risk_analysis'].lower()
        self.financial_risk = inputs['financial_risk_analysis'].lower()
        self.risk_free_rate = inputs['risk_free_rate']

        self.bond_spread = inputs['bond_spread']
        self.tax_rate = inputs['tax_rate']

        self.high_business_risk = {
            'low': 0.064,
            'medium': 0.075, 
            'high': 0.09
        }
        self.med_business_risk = {
            'low': 0.04,
            'medium': 0.05, 
            'high': 0.061
        }
        self.low_business_risk = {
            'low': 0.02,
            'medium': 0.03, 
            'high': 0.039
        }

        self.compute_equity_risk_premium()
        self.compute_cost_of_equity()
        self.compute_after_tax_cost_of_debt()
        self.compute_wacc()

    def compute_equity_risk_premium(self):
        if self.business_risk == 'high':
            self.erp = self.high_business_risk[self.financial_risk]
        elif self.business_risk == 'medium':
            self.erp = self.med_business_risk[self.financial_risk]
        elif self.business_risk == 'low':
            self.erp = self.low_business_risk[self.financial_risk]
        else:
            raise ValueError('Please enter a valid string (high, med, low).')

    def compute_cost_of_equity(self): 
        """
        Computes the Cost of Equity.
        """
        self.cost_of_equity = self.risk_free_rate + self.erp

    def compute_after_tax_cost_of_debt(self):
        """
        Computes the Cost of Debt.
        """
        self.risk_free_rate_spread = self.risk_free_rate + self.bond_spread
        self.cost_of_debt = round(self.risk_free_rate_spread * (1 - self.tax_rate), 2)
        self.after_tax_cost_of_debt = self.cost_of_debt * (1 - self.tax_rate)
    
    def compute_wacc(self):
        """
        Computes the Weight Average Cost of Capital. 
        """
        self.wacc = round((self.after_tax_cost_of_debt * self.percent_debt) + (self.cost_of_equity * self.percent_equity), 3)
        return self.wacc

# Testing 

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

test = WeightedAvgCostCapital(inputs=inputs)"""

        
    

        

    

