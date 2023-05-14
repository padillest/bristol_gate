import streamlit as st
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, data):
        fig, ax = plt.subplots()
        ax.set_title('Simulated Share Price')
        ax.hist(data, bins=5)
        st.pyplot(fig)