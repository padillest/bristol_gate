from WACC import WeightedAvgCostCapital
import pandas as pd

class DCF:
    def __init__(self, 
                 inputs: dict) -> pd.DataFrame:
        # store user inputs
        self.inputs = inputs
        self.final_yr = self.inputs['yrs'][-1]
        self.projection_period = len(self.inputs['yrs']) - 1
        self.inputs['wacc'] = WeightedAvgCostCapital(inputs=inputs).wacc

        # store data outputs/dataframes
        self.dcf_df = pd.DataFrame(columns=['projected_revenue'])
        self.exit_multiple_method_df = pd.DataFrame(columns=['terminal_value'])

        # run DCF calculations
        self.compute_projected_revenue()
        self.compute_ebitda()
        self.compute_depreciation_amortization()
        self.compute_ebit()
        self.compute_unlevered_free_cash_flow()
        self.compute_present_value_ufcf()
        self.compute_exit_multiple_table()

    def compute_projected_revenue(self) -> None:
        """
        Computes the Projected Revenue.
        
        Computes the Projected Revenue according to User Inputs, 
        specifically, the previous year's revenue and the year growth. 
        
        Args: 
            None.
        
        Returns:
            A pandas Series of Projected Revenue. 
        """
        previous_revenue = self.inputs['previous_yr_revenue']
        growth_percent = self.inputs['yr_growth']
        # loop to reference the previous year's projected revenue
        for i in self.inputs['yrs']:
            new_val = previous_revenue * (1 + growth_percent)
            previous_revenue = new_val
            self.dcf_df.loc[len(self.dcf_df)] = new_val

    def compute_ebitda(self) -> None:
        """
        Computes the EBITDA.
        
        Computes the EBITDA according to the pandas Series of Projected Revenue and 
        the EBITDA margins. Note that the EBITDA margins are simulated in each DCF 
        simulation. 

        Args: 
            None
        Returns:
            A pandas Series of each projected year's EBITDA
        """
        self.dcf_df['ebitda'] = self.inputs['ebitda_margin'] * self.dcf_df['projected_revenue']

    def compute_depreciation_amortization(self):
        """
        Compute the D&A according to an assumption and the Projected Revenue.
        
        Args:
            None
            
        Returns: 
            A pandas Series of each projected year's D&A
        """
        self.dcf_df['dna'] = self.inputs['dna'] * self.dcf_df['projected_revenue']

    def compute_ebit(self) -> None:
        """
        Compute the Operating Income according to the EBITDA and the EBIT margin.
        
        Args: 
            None 
            
        Returns:
            A pandas Series of EBIT
        """
        self.dcf_df['ebit'] = self.dcf_df['ebitda'] - self.dcf_df['dna']

    def compute_projected_taxes(self) -> None:
        """
        Compute the Taxes for the projected years.
        
        Args: 
            None 

        Returns:
            A pandas Series of Taxes
        """
        self.dcf_df['tax'] = self.dcf_df['ebit'] * self.inputs['tax_percent']


    def compute_capex(self) -> None:
        """
        Compute the Capital Expenditure.
        
        Args:
            None
        
        Returns:
            A pandas Series of the projected CapEx
        """
        self.dcf_df['capex'] = self.dcf_df['projected_revenue'] * self.inputs['capex_percent']
    
    def compute_nwc(self) -> None:
        """Compute Net Working Capital.
        
        Args:
            None
        
        Returns:
            A pandas Series of the Net Working Capital
        """
        self.dcf_df['net_working_capital'] = self.dcf_df['projected_revenue'] * self.inputs['nwc_percent']
        
    def compute_unlevered_free_cash_flow(self) -> None:
        """
        Compute the Unlevered Free Cash Flow using EBITDA, Taxes, Capital Expenditure, and 
        Change in Net Working Capital.
        
        Args: 
            None 
            
        Returns: 
            A pandas Series of the Unlevered Free Cash Flow   
        """
        self.compute_projected_taxes()
        self.compute_capex()
        self.compute_nwc()

        self.dcf_df['unlevered_free_cash_flow'] = (self.dcf_df['ebitda'] 
                                                   - self.dcf_df['tax'] 
                                                   - self.dcf_df['capex']
                                                   - self.dcf_df['net_working_capital'])

    def compute_discount_factor(self) -> None:
        """
        Computes the Discount Factor.
        
        Args: 
            None
        
        Returns: 
            A pandas Series of the Discount Factor for each projected year.
            
        """
        for idx in self.dcf_df.index: 
            val = (1 / (1 + self.inputs['wacc']) ** (idx + 1))
            self.dcf_df.at[idx, 'discount_factor'] = val


    def compute_present_value_ufcf(self) -> None:
        """
        Computes the Present Value Unlevered Free Cash Flow.
        
        Args: 
            None 
        
        Returns: 
            A pandas Series of the the projected year's Unlevered Free Cash Flow
        """
        self.compute_discount_factor()
        self.dcf_df['pv_ufcf'] = self.dcf_df['unlevered_free_cash_flow'] * self.dcf_df['discount_factor']

    def compute_terminal_value(self) -> None:
        """
        Computes the Terminal Value for the Exit Multiple Method.

        Args: 
            None
        
        Returns: 
            A pandas Series of the Terminal Value
        """
        self.final_ebitda = self.dcf_df['ebitda'].iloc[len(self.dcf_df)-1]
        self.exit_multiple_method_df.loc[len(self.exit_multiple_method_df)] = self.final_ebitda * self.inputs['exit_multiple']

    def compute_present_terminal_value(self) -> None:
        """
        Computes the Present Terminal Value.

        Args: 
            None
        
        Returns: 
            A pandas Series of the Present Value Terminal Value according to the WACC calculation
        """
        self.exit_multiple_method_df['pv_tv'] = self.exit_multiple_method_df['terminal_value'] / ((1 + self.inputs['wacc']) ** self.projection_period)

    def compute_cumulative_pv_ufcf(self) -> None:
        """
        Computes the cumulative present value of the Unlevered Free Cash Flow.
        
        Args:
            None
        
        Returns: 
            A pandas Series of the cumuative Unlevered Free Cash Flow
        """
        self.exit_multiple_method_df['sum_pv_ufcf'] = self.dcf_df['pv_ufcf'].sum()

    def compute_implied_enterprise_value(self) -> None:
        """
        Computes the Implied Enterprise Value.
        
        Args: 
            None 
        
        Returns: 
            A pandas Series of the Implied Enterprise Value
        """
        self.compute_present_terminal_value()
        self.compute_cumulative_pv_ufcf()
        self.exit_multiple_method_df['implied_enterprise_value'] = (self.exit_multiple_method_df['sum_pv_ufcf'] 
                                                                    + self.exit_multiple_method_df['pv_tv'])

    def compute_implied_equity_value(self) -> None:
        """
        Computes the Implied Equity Value.
        
        Args: 
            None 
        
        Returns: 
            A pandas Series of the Implied Equity Value
        """
        self.exit_multiple_method_df['implied_equity_value'] = (self.exit_multiple_method_df['implied_enterprise_value'] 
                                                                + self.inputs['cash'] 
                                                                - self.inputs['debt'])

    def compute_implied_share_price(self) -> None:
        """Computes the Implied Share Price.
        
        Args:
            None
        
        Returns: 
            A pandas Series of implied share prices
        """
        self.exit_multiple_method_df['implied_share_price'] = self.exit_multiple_method_df['implied_equity_value'] / self.inputs['shares_outstanding']

    def compute_safety_margin(self) -> None:
        """
        Computes the Safety Margin of a Company.
        
        Args: 
            None 
        
        Returns: 
            A pandas Series of the Safety Margin percentage
        """
        self.exit_multiple_method_df['safety_margin'] = 1 - (self.inputs['current_share_price']/self.exit_multiple_method_df['implied_share_price'])

    def compute_exit_multiple_table(self):
        """
        Computes the Exit Multiple Method table.
        
        Args: 
            None 
        
        Returns: 
            None
        """
        self.compute_terminal_value()
        self.compute_present_terminal_value()
        self.compute_implied_enterprise_value()
        self.compute_implied_equity_value()
        self.compute_implied_share_price()
        self.compute_safety_margin()


    

