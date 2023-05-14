import streamlit as st
import datetime
import itertools
from MonteCarlo import MonteCarlo

class UserInputs:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.create_headings()
        self.create_columns()
        self.add_inputs()

        if self.confirm:
            # Store all data and pass as input
            self.store_inputs()

    def create_headings(self):
        st.title('Monte Carlo Discounted Cash Flow Model')
        st.subheader('Input model values')

    def create_columns(self):
        self.c1_a, self.c2_a =  st.columns(2)
        self.c1_b, self.c2_b, self.c3_b = st.columns(3)

    def add_inputs(self):
        with self.c1_a:
            self.iterations = st.slider(label='Specify the number of iterations:',
                                        min_value=1,
                                        max_value=1000,
                                        value=500)
            self.business_risk = st.radio(label='Select the Business Risk:',
                                    options=['Low', 'Medium', 'High'])         
        with self.c2_a:
            self.yrs = st.slider(label='Specify the number of years:',
                            min_value=1,
                            max_value=10)
            self.financial_risk = st.radio(label='Select the Financial Risk:',
                                    options=['Low', 'Medium', 'High'])    
        with self.c1_b:
            self.risk_free_rate = st.number_input(label='Specify the Risk-Free Rate:')
            self.equity = st.number_input(label='Specify the company\'s Equity:')
            self.shares_outstanding = st.number_input(label='Specify the number of Outstanding Shares:')
            self.previous_yr_revenue = st.number_input(label='Specify the company\'s previous year revenue:')
            self.capex = st.number_input(label='Specify the company\'s CapEx percentage:')
            self.confirm = st.button(label='Confirm')
        with self.c2_b:
            self.bond_spread = st.number_input(label='Specify the Bond Spread:')
            self.cash = st.number_input(label='Specify the company\'s cash:')
            self.dna = st.number_input(label='Specify the company\'s D&A percentage:')
            self.nwc = st.number_input(label='Specify the company\'s Net Working Capital percentage:')
        with self.c3_b:
            self.tax_rate = st.number_input(label='Specify the Tax Rate:')
            self.share_price = st.number_input(label='Specify the company\'s Share Price:')
            self.debt = st.number_input(label='Specify the company\'s debt:')
            self.tax_percent = st.number_input(label='Specify the tax percentage:')
        
    def store_inputs(self):
        current_yr = datetime.date.today().year
        yr_list = [] 
        for i in range(self.yrs): 
            yr_list.append(current_yr + i + 1)

        self.dna_dict = self.create_dictionary_pairs(yr_list=yr_list, val=self.dna)
        self.tax_dict = self.create_dictionary_pairs(yr_list=yr_list, val=self.tax_percent)
        self.capex_dict = self.create_dictionary_pairs(yr_list=yr_list, val=self.capex)
        self.nwc_dict = self.create_dictionary_pairs(yr_list=yr_list, val=self.nwc)

        self.inputs = {
            'business_risk_analysis': self.business_risk.lower(),
            'financial_risk_analysis': self.financial_risk.lower(),
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
            'dna': self.dna_dict,
            'tax_percent': self.tax_dict,
            'capex_percent': self.capex_dict,
            'nwc_percent': self.nwc_dict,
        }


    def create_dictionary_pairs(self, yr_list, val):
        val_list = list(itertools.repeat(float(val), len(yr_list)))
        return dict(zip(yr_list, val_list))
