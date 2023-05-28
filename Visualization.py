import streamlit as st
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, data):
        """Class attributes"""
        # create plots 
        fig, ax = plt.subplots()
    
        # create title and plot
        ax.set_title('Simulated Share Price')
        ax.hist(data['implied_share_price'], bins=8)
        st.pyplot(fig)