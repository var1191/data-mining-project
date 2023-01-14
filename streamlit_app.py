import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

st.title('Real-Time Prediction and Visualization')

df = pd.read_csv('final_df.csv')

st.dataframe(df, index=False)




