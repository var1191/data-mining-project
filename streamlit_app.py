import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

st.title('Real-Time Prediction and Visualization')

# Read the dataset
st.markdown('This is our dataset after preprocessing.')
new_df = pd.read_csv('final_df.csv')
st.dataframe(new_df.head())


#===================================================
# Linear Regression
st.markdown('## Linear Regression Model for Prediction of TotalSpent_RM')

df_reg = new_df.copy()
df_reg = df_reg.drop(columns=['Date', 'Time'])
df_reg = df_reg.drop(columns=df_reg.columns[0])

st.markdown('We use all the variable except Date and Time.')
st.dataframe(df_reg.head())




