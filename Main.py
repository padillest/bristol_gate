import streamlit as st
from UserInputs import UserInputs
from MonteCarlo import MonteCarlo
from Visualization import Visualization
import pandas as pd

def main(): 
    user_inputs = UserInputs()
    if user_inputs.confirm:
        mc_obj = MonteCarlo(user_inputs.iterations, 
                            inputs=user_inputs.inputs,
                            data='./dcf_data.xlsx')
        df = pd.DataFrame(mc_obj.simulated_share_price, columns=['simulated_share_price'])
        Visualization(data=df)

if __name__ == '__main__':
    main()