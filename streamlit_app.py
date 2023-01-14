import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

st.title('Real-Time Prediction and Visualization')

# Read the dataset
new_df = pd.read_csv('final_df.csv')

# Linear Regression
st.markdown('## Linear Regression Model for Prediction of TotalSpent_RM')




