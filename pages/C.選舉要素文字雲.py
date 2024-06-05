import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
features = ['us_relation_opinion', 'china_relation_opinion',
            'international_alignment_opinion', 'china_democracy_destruction_opinion',
            'taiwan_improvement_opinion', 'taiwan_political_fighting_opinion',
            'democracy_satisfaction', 'future_democracy_prospects']
dataset = pd.read_csv('datas.csv')
sc = StandardScaler()
standard =sc.fit_transform(dataset[features])
standard_data = pd.DataFrame(standard, columns=features)
standard_dataset = pd.concat([dataset.drop(columns=features), standard_data], axis=1)
choose_dic={
    '性別':'gender','學院':'college','年級':'grade','年齡':'age',
    '戶籍地':'residence','在意身邊的朋友親中嗎?':'friend_pro_china','在意伴侶親中嗎?':'marriage_pro_china',
    '民族認同':'self_identity','家庭慣用語言':'family_language','朋友親中比例':'friend_pro_china_ratio',
    '兩岸關係':'taiwan_china_relation','是否贊成和民主化後中國統一':'support_unification_if_democratic',
    '認為選舉最重要的是?':'most_important_democracy_aspect','參與候選人或政黨活動頻率':'election_volunteer',
    '是否勸說他人支持特定候選人':'election_persuasion','是否認為意識型態長期凌駕於內政問題？':'ideology_over_domestic_issues',
    '2024總統投給誰':'candidate_voted_for','2024不分區投給哪個政黨':'party_supported'
}
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.font_manager import FontProperties as font
import matplotlib.patches as patches
import matplotlib
import time
st.subheader('文字雲')

font1 = font(fname="msjhbd.ttc")
def draw_wordcloud(dataset, feature, type):
    data_presidential_candidate = dataset.groupby(feature).get_group(type).iloc[:, 26]
    data_party_vote = dataset.groupby(feature).get_group(type).iloc[:, 27]
    data_regional_legislator = dataset.groupby(feature).get_group(type).iloc[:, 28]

    # Splitting data and creating text for presidential candidates
    split_presidential_candidate = data_presidential_candidate.str.split(',', expand=True)
    split_presidential_candidate = split_presidential_candidate.fillna(' ')
    split_presidential_candidate = split_presidential_candidate.astype(str).values.flatten()
    text_presidential = ' '.join(split_presidential_candidate)

    # Splitting data and creating text for party vote
    split_party_vote = data_party_vote.str.split(',', expand=True)
    split_party_vote = split_party_vote.fillna(' ')
    split_party_vote = split_party_vote.astype(str).values.flatten()
    text_party_vote = ' '.join(split_party_vote)

    # Splitting data and creating text for regional legislator
    split_regional_legislator = data_regional_legislator.str.split(',', expand=True)
    split_regional_legislator = split_regional_legislator.fillna(' ')
    split_regional_legislator = split_regional_legislator.astype(str).values.flatten()
    text_regional_legislator = ' '.join(split_regional_legislator)

    # Word cloud for presidential candidates
    wordcloud_presidential = WordCloud(width=1280, height=720, background_color='white',
                                       font_path="msjhbd.ttc").generate(text_presidential)
    fig_presidential, ax_presidential = plt.subplots(figsize=(10, 5))
    ax_presidential.imshow(wordcloud_presidential, interpolation='bilinear')
    ax_presidential.axis('off')
    fig_presidential.patch.set_facecolor('#4286F3')
    plt.rcParams['font.family'] = 'Microsoft JhengHei'
    #ax_presidential.set_title("選擇總統最重要的因素", fontsize=40, color='white', fontweight='bold')

    # Word cloud for party vote
    wordcloud_party_vote = WordCloud(width=1280, height=720, background_color='white',
                                     font_path="msjhbd.ttc").generate(text_party_vote)
    fig_party_vote, ax_party_vote = plt.subplots(figsize=(10, 5))
    ax_party_vote.imshow(wordcloud_party_vote, interpolation='bilinear')
    ax_party_vote.axis('off')
    fig_party_vote.patch.set_facecolor('#EB4537')
    plt.rcParams['font.family'] = 'Microsoft JhengHei'
    #ax_party_vote.set_title("選擇政黨最重要的因素", fontsize=40, color='white', fontweight='bold')

    # Word cloud for regional legislator
    wordcloud_regional_legislator = WordCloud(width=1280, height=720, background_color='white',
                                               font_path="msjhbd.ttc").generate(text_regional_legislator)
    fig_regional_legislator, ax_regional_legislator = plt.subplots(figsize=(10, 5))
    ax_regional_legislator.imshow(wordcloud_regional_legislator, interpolation='bilinear')
    ax_regional_legislator.axis('off')
    fig_regional_legislator.patch.set_facecolor('#FAC230')
    plt.rcParams['font.family'] = 'Microsoft JhengHei'
    #ax_regional_legislator.set_title("選擇區域立委最重要的因素", fontsize=40, color='white', fontweight='bold')

    # Displaying the plots using Streamlit
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1, f'Producing plots... {i + 1}%')
        time.sleep(0.05)
    bar.progress(100, 'Done!')
    st.subheader('選擇總統最重要的因素')
    st.pyplot(fig_presidential)
    st.subheader('選擇政黨最重要的因素')
    st.pyplot(fig_party_vote)
    st.subheader('選擇區域立委最重要的因素')
    st.pyplot(fig_regional_legislator)

option_3 = st.selectbox("",
   ('性別', '學院', '年級', '年齡', '戶籍地', '在意身邊的朋友親中嗎?',
    '在意伴侶親中嗎?', '民族認同', '家庭慣用語言', '朋友親中比例', '兩岸關係', '是否贊成和民主化後中國統一',
    '認為選舉最重要的是?', '參與候選人或政黨活動', '是否勸說他人支持特定候選人', '是否認為意識型態長期凌駕於內政問題？',
    '2024總統投給誰', '2024不分區投給哪個政黨'),
   index=None,
   placeholder="請選擇要分析的要素...",
   key="option_3"
)
if choose_dic.get(option_3) is not None :
    group_names = list(dataset.groupby(choose_dic.get(option_3)).groups.keys())
    option_4 = st.selectbox("",
    group_names,
    index=None,
    placeholder="請選擇要分析的類別...",
    key="option_4"
    )
    st.write("You selected:", option_3,option_4)

    if option_3 is not None and option_4 is not None :
        draw_wordcloud(dataset, choose_dic.get(option_3),option_4)

    else:
        st.info("請選擇有效的索引。")
