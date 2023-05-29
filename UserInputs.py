import streamlit as st
import datetime
import itertools
from MonteCarlo import MonteCarlo

class UserInputs:
    def __init__(self):
        """Class attributes"""

        # create UI layout
        st.set_page_config(layout="wide")
        self.create_headings()
        self.create_columns()
        self.add_inputs()

        # if the 'Confirm' button is pressed
        if self.confirm:
            # store all data and pass as input
            self.store_inputs()

    def create_headings(self):
        """
        Create the headings within the UI. 

        Args: 
            None 

        Returns:
            None 
        """
        st.title('Monte Carlo Discounted Cash Flow Model')
        st.subheader('Input model values')

    def create_columns(self):
        """
        Create the columns within the UI. 

        Args: 
            None 

        Returns:
            None 
        """
        self.c1_a, self.c2_a =  st.columns(2)
        self.c1_b, self.c2_b, self.c3_b = st.columns(3)

    def add_inputs(self):
        """
        Create the User Input blocks.

        Args: 
            None 

        Returns:
            None 
        """
        # create inputs in the first column in the first tier
        with self.c1_a:
            self.iterations = st.slider(label='Specify the number of iterations:',
                                        min_value=1,
                                        max_value=10000,
                                        value=5000)
            self.business_risk = st.radio(label='Select the Business Risk:',
                                    options=['Low', 'Medium', 'High'])   
        # create inputs in the second column in the first tier  
        with self.c2_a:
            self.yrs = st.slider(label='Specify the number of years:',
                            min_value=1,
                            max_value=10)
            self.optimal_capital_structure = st.number_input(label='Specify the Target Optimal Capital Structure (%):')   
        # create inputs in the first column in the second tier
        with self.c1_b:
            self.risk_free_rate = st.number_input(label='Specify the Risk-Free Rate:')
            self.equity = st.number_input(label='Specify the company\'s Equity:')
            self.shares_outstanding = st.number_input(label='Specify the number of Outstanding Shares:')
            self.previous_yr_revenue = st.number_input(label='Specify the company\'s previous year revenue:')
            self.capex = st.number_input(label='Specify the company\'s CapEx percentage:')
            self.confirm = st.button(label='Confirm')
        # create inputs in the second column in the second tier    
        with self.c2_b:
            self.bond_spread = st.number_input(label='Specify the Bond Spread:')
            self.cash = st.number_input(label='Specify the company\'s cash:')
            self.dna = st.number_input(label='Specify the company\'s D&A percentage:')
            self.nwc = st.number_input(label='Specify the company\'s Net Working Capital percentage:')
        # create inputs in the first column in the second tier
        with self.c3_b:
            self.tax_rate = st.number_input(label='Specify the Tax Rate:')
            self.share_price = st.number_input(label='Specify the company\'s Share Price:')
            self.debt = st.number_input(label='Specify the company\'s debt:')
            self.tax_percent = st.number_input(label='Specify the tax percentage:')
        
    def store_inputs(self):
        """
        Store the User Inputs in a dictionary. 
        
        Args: 
            None 
        
        Returns: 
            A dictionary of User Input values 
        """
        # store the current year
        current_yr = datetime.date.today().year
        yr_list = [] 
        # create a list of projection years 
        for i in range(self.yrs): 
            yr_list.append(current_yr + i + 1)
        # store User Inputs in a dictionary
        self.inputs = {
            'business_risk_analysis': self.business_risk.lower(),
            'target_optimal_capital_structure': self.optimal_capital_structure,
            'risk_free_rate': self.risk_free_rate, 
            'bond_spread': self.bond_spread,
            'tax_rate': self.tax_rate, 
            'equity': self.equity, 
            'current_share_price': self.share_price,
            'shares_outstanding': self.shares_outstanding,
            'cash': self.cash,
            'debt': self.debt,
            'yrs': yr_list,
            'previous_yr_revenue': self.previous_yr_revenue,
            'dna': self.dna,
            'tax_percent': self.tax_percent,
            'capex_percent': self.capex,
            'nwc_percent': self.nwc,
        }
