import streamlit as st
import pandas as pd
dataset = pd.read_csv('datas.csv')

dataset['us_relation_opinion'] = 1+(dataset['us_relation_opinion']-1)*1.5

st.write(dataset)