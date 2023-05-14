import itertools
import DCF
import numpy as np
import pandas as pd

class MonteCarlo: 
    def __init__(self, n: int, inputs: dict, data: pd.DataFrame, ticker='GPS-US') -> dict:
        """Class attributes"""
        self.n = n
        self.inputs = inputs
        self.ticker = ticker.upper()

        # Ingest and process data
        self.data = pd.read_excel(data)
        self.process_data()

        self.simulated_share_price = []
        self.simulated_projected_growth = []
        self.simulated_terminal_value_multiples = []
        self.simulated_ebitda_margins = []

        self.run_monte_carlo()

    def process_data(self) -> None: 
        """
        Process any input dataset containing 
        """
        self.data['year'] = self.data['date'].dt.year
        self.data['month'] = self.data['date'].dt.month
        self.data['day'] = self.data['date'].dt.day
        self.data['projected_revenue'] = round(self.data.groupby('ticker')['revenue'].pct_change(), 3)
        self.data = self.data.dropna().reset_index(drop=True)

        # Process the projected growth from the quarterly data

        self.ticker_data = self.data[self.data['ticker'] == self.ticker]
        
    def zip_scalar(self, l: list, s: float) -> dict:
        """
        Zips a scalar with a list to 
        produce a dictionary.
        """
        s_list = list(itertools.repeat(float(s), len(l)))
        return dict(zip(l, s_list))
    
    def generate_random_value(self, mean: float, 
                              std: float, decimal: int) -> None: 
        """
        Returns a random value according to a 
        Normal distribution, mean, and standard
        deviation.
        """
        generated_val = float(np.random.normal(
            loc=mean,
            scale=std,
            size=1
        ).round(decimal))

        return generated_val

    def generate_random_dict(self, generated_val: float) -> None:
        """
        Returns an updated dictionary of 
        inputs according to a simulated
        value.
        """
        generated_dict = self.zip_scalar(
            l=self.inputs['yrs'],
            s=generated_val
        )
        return generated_dict

    def update_inputs(self):
        """
        Updates the inputs to include the simulated 
        values.
        """
        self.generated_ebitda_margin = round(float(self.sampled_data['ebitda_margin']), 3) # should be changed depending on dataset
        self.generated_projected_growth = float(self.sampled_data['projected_revenue']) #self.generate_random_value(mean=0.5, std=0.2, decimal=3)
        self.generated_terminal_value_multiple = self.generate_random_value(mean=6, std=3, decimal=0)

        self.ebitda_margin_dict = self.generate_random_dict(generated_val=self.generated_ebitda_margin)
        self.projected_growth_dict = self.generate_random_dict(generated_val=self.generated_projected_growth)

        self.inputs.update(ebitda_margin=self.ebitda_margin_dict)
        self.inputs.update(yr_growth=self.projected_growth_dict)
        self.inputs.update(exit_multiple=self.generated_terminal_value_multiple)
    
    def run_single_simulation(self):
        """
        Runs a single DCF simulation using
        randomly generated values.
        """
        self.sampled_data = self.ticker_data.sample()
        self.update_inputs()
    
    def run_monte_carlo(self):
        """
        Runs the Monte Carlo simulation and creates 
        a DCF object.
        """
        for i in range(self.n): 
            self.run_single_simulation()
            self.simulated_projected_growth.append(self.generated_projected_growth)
            self.simulated_ebitda_margins.append(self.generated_ebitda_margin)
            self.simulated_terminal_value_multiples.append(self.generated_terminal_value_multiple)
            model = DCF.DCF(self.inputs)
            self.simulated_share_price.append(model.implied_share_price)

        return round(sum(self.simulated_share_price) / self.n, 2)



    
# Testing 

"""inputs = {
    'business_risk_analysis': 'low',
    'financial_risk_analysis': 'low',
    'risk_free_rate': 0.0396,
    'bond_spread': 0.0161,
    'tax_rate': 0.207,
    'equity': 3000,
    'current_share_price': 14, 
    'shares_outstanding': 1000, 
    'cash': 1215,
    'debt': 6200, 
    #'wacc': 0.1, 
    'yrs': [2024, 2025, 2026],
    'previous_yr_revenue': 2200,
    #'yr_growth': {2024: 0.02, 2025: 0.02, 2026: 0.02}, 
    #'ebitda_margin': {2024: 0.05, 2025: 0.05, 2026: 0.05},
    'dna': {2024: 0.034, 2025: 0.034, 2026: 0.034}, 
    'tax_percent': {2024: 0.14, 2025: 0.14, 2026: 0.14},
    'capex_percent': {2024: 0.04, 2025: 0.04, 2026: 0.04},
    'nwc_percent': {2024: 0.01, 2025: 0.01, 2026: 0.01}
}

test = MonteCarlo(n=5, inputs=inputs, data='./dcf_data.xlsx')
print(test.simulated_share_price)"""