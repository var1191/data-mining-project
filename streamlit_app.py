import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title = 'Real-Time Prediction and Visualization',
    layout = 'wide'
)
st.title('Real-Time Prediction and Visualization')


# Read the dataset
st.markdown('This is our dataset after preprocessing.')
new_df = pd.read_csv('final_df.csv')
new_df = new_df.drop(columns= new_df.columns[0])
st.dataframe(new_df.head())


#===================================================
# Linear Regression
st.markdown('## Linear Regression Model')

st.markdown('At this part we use all the variable except Date and Time.')
df_reg = new_df.copy()
df_reg = df_reg.drop(columns=['Date', 'Time'])
st.dataframe(df_reg.head())

choice_list = ['TotalSpent_RM']
choice_list.append(df_reg.columns)

# select a column as 'Y'
choice_reg = st.selectbox('Choose a variable to predict:', np.unique(choice_list))

# Dummify it
X = df_reg.loc[:, df_reg.columns != choice_reg] 
Y = df_reg.loc[:, df_reg.columns == choice_reg] 

le = LabelEncoder()
dfReg_label_dict = {} # to get the label detail

# if 'Y' is Object, encode it using Label Encoder
if df_reg[choice_reg].dtype == 'O':
    dfReg_label_dict[choice_reg] = {}
    Y = le.fit_transform(Y)
    dfReg_label_dict[choice_reg].update(dict(zip(le.classes_, range(len(le.classes_)))))

X = pd.get_dummies(data=X)

# Model Construction
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=101)
