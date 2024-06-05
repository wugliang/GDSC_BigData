import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="政知道了",page_icon=":bar_chart:")

st.title('政知道了')
st.header('成大學生政治分析器')
url = "https://www.facebook.com/gdscncku"
st.write(f"[Designed and developed by GDSC BigData 2024]({url})")
st.write('數據僅供參考')
dataset = pd.read_csv('datas.csv')
st.subheader('樣本總數')
st.header(dataset.shape[0])
st.subheader('性別概況')
data_counts = dataset.groupby('gender').size().reset_index(name='count')
fig = px.pie(data_counts, values='count', names='gender')
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)
st.subheader('戶籍地概況')
residence_counts = dataset['residence'].value_counts().reset_index()
residence_counts.columns = ['residence', 'count']
fig = px.treemap(residence_counts, path=[px.Constant("all"), 'residence'], values='count')
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
st.plotly_chart(fig)
st.subheader('年齡概況')
age_counts = dataset['age'].value_counts().reset_index()
age_counts.columns = ['age', 'count']
# 創建條形圖
fig = px.bar(age_counts, x='age', y='count', labels={'age': '年齡', 'count': '人數'})
# 在 Streamlit 中顯示圖表
st.plotly_chart(fig)

st.subheader('學院分布概況')
college_counts = dataset['college'].value_counts().reset_index()
college_counts.columns = ['college', 'count']
fig_hbar = px.bar(college_counts, x='count', y='college', orientation='h', labels={'college': '學院', 'count': '人數'})
# 在 Streamlit 中顯示圖表
st.plotly_chart(fig_hbar)
st.write('點擊面板前往Power BI')
components.iframe("https://docs.google.com/presentation/d/e/2PACX-1vTB5-E_E4e2kcZsN7mLUSV43E58ii2b9GhesSw4sTq0u928eKboMTtd1M2VspoY1A/embed?start=false&loop=true&delayms=3000", height=480)