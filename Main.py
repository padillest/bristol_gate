import streamlit as st
from UserInputs import UserInputs
from MonteCarlo import MonteCarlo
from Visualization import Visualization
import pandas as pd

def main(): 
    # create the interface to collect User inputs
    user_inputs = UserInputs()

    # if the 'Confirm' button is pressed
    if user_inputs.confirm:
        # create an instance of the Monte Carlo object
        mc_obj = MonteCarlo(n=user_inputs.iterations, 
                            inputs=user_inputs.inputs,
                            data='./dcf_data.xlsx') # make changes to this line if the dataset exists elsewhere
        # create a dataframe of the simulated share prices 
        inputs = mc_obj.simulated_dcfs
        exit = mc_obj.simulated_exit_multiple_method
        df = pd.DataFrame(exit['implied_share_price'])
        # call an instance of the Visualization object
        Visualization(data=df)

if __name__ == '__main__':
    main()