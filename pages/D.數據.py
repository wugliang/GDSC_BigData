import streamlit as st
import pandas as pd
st.set_page_config(page_title="政知道了",page_icon=":bar_chart:")
dataset = pd.read_csv('datas.csv')

dataset['us_relation_opinion'] = 1+(dataset['us_relation_opinion']-1)*1.5

st.write(dataset.drop(dataset.columns[0], axis=1))
