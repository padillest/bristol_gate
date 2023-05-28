class WeightedAvgCostCapital: 
    # Dictionaries of Equity Risk Premiums

    def __init__(self,
                 inputs: dict) -> float:
        """
        Establish the ERP of a Company using a Weighted Average Cost of Capital (WACC) table.

        Args: 
            inputs: A dictionary of User Inputs
        
        Returns: 
            A Weighted Average Cost of Capital
        """

        # compute the total value 
        self.equity = inputs['equity']
        self.debt = inputs['debt']
        self.total_value = self.equity + self.debt

        # compute percentages
        self.percent_equity = self.equity / self.total_value
        self.percent_debt = self.debt / self.total_value

        # alter inputs
        self.business_risk = inputs['business_risk_analysis'].lower()
        self.financial_risk = inputs['financial_risk_analysis'].lower()

        # store other inputs
        self.risk_free_rate = inputs['risk_free_rate']
        self.bond_spread = inputs['bond_spread']
        self.tax_rate = inputs['tax_rate']

        # business risk dictionaries
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

        # functions to compute WACC
        self.compute_equity_risk_premium()
        self.compute_cost_of_equity()
        self.compute_after_tax_cost_of_debt()
        self.compute_wacc()

    def compute_equity_risk_premium(self):
        """
        Computes the Equity Risk Premium (ERP) according to User Inputs.

        Args:
            None
        
        Returns:
            An ERP value according to the inputted Business and Financial Risk
        """
        if self.business_risk == 'high':
            self.erp = self.high_business_risk[self.financial_risk]
        elif self.business_risk == 'medium':
            self.erp = self.med_business_risk[self.financial_risk]
        else:
            self.erp = self.low_business_risk[self.financial_risk]

    def compute_cost_of_equity(self): 
        """
        Computes the Cost of Equity.

        Args: 
            None 
        
        Returns: 
            A Cost of Equity calculation
        """
        self.cost_of_equity = self.risk_free_rate + self.erp

    def compute_after_tax_cost_of_debt(self):
        """
        Computes the Cost of Debt.

        Args:
            None
        
        Returns: 
            An After Tax Cost of Debt calculation
        """
        self.risk_free_rate_spread = self.risk_free_rate + self.bond_spread
        self.cost_of_debt = round(self.risk_free_rate_spread * (1 - self.tax_rate), 2)
        self.after_tax_cost_of_debt = self.cost_of_debt * (1 - self.tax_rate)
    
    def compute_wacc(self):
        """
        Computes the Weight Average Cost of Capital (WACC).

        Args:
            None 

        Returns: 
            A WACC calculation 
        """
        self.wacc = round((self.after_tax_cost_of_debt * self.percent_debt) + (self.cost_of_equity * self.percent_equity), 3)
        return self.wacc

        
    

        

    

