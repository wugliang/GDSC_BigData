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

st.subheader('儀表圖')
choose_dic={
    '性別':'gender','學院':'college','年級':'grade','年齡':'age',
    '戶籍地':'residence','在意身邊的朋友親中嗎?':'friend_pro_china','在意伴侶親中嗎?':'marriage_pro_china',
    '民族認同':'self_identity','家庭慣用語言':'family_language','朋友親中比例':'friend_pro_china_ratio',
    '兩岸關係':'taiwan_china_relation','是否贊成和民主化後中國統一':'support_unification_if_democratic',
    '認為選舉最重要的是?':'most_important_democracy_aspect','參與候選人或政黨活動頻率':'election_volunteer',
    '是否勸說他人支持特定候選人':'election_persuasion','是否認為意識型態長期凌駕於內政問題？':'ideology_over_domestic_issues',
    '2024總統投給誰':'candidate_voted_for','2024不分區投給哪個政黨':'party_supported'
}
def plot_gauge(dataset, features,choose_A1,choose_A2,choose_B1,choose_B2,Range):
    width = 800  
    height = 150  
    rows = len(features)
    features_dict = {
        'us_relation_opinion': '向美國靠近是好事嗎?',
        'china_relation_opinion': '向中國靠近是好事嗎?',
        'international_alignment_opinion': '臺灣在國際關係上要向其他國家靠攏嗎?',
        'china_democracy_destruction_opinion': '中國在破壞台灣的民主嗎?',
        'taiwan_improvement_opinion':'這幾年台灣越來越好?',
        'taiwan_political_fighting_opinion': '近年臺灣政治惡鬥愈加嚴重？',
        'democracy_satisfaction': '對目前臺灣民主政治運作的滿意程度',
        'future_democracy_prospects': '對於台灣未來民主政治的信心',
    }

    # 創建子圖布局,TYPE='domain'
    fig = make_subplots(
        rows=rows, 
        cols=1, 
        subplot_titles=list(features_dict.values()),
        specs=[[{"type": "domain"}] for _ in range(rows)]
    )
    for i in range(rows):
        fig.layout.annotations[i].update(x=0, xanchor='left', align='left')
    # 篩選資料集
    filtered_dataset = dataset.copy()
    filtered_dataset = dataset.loc[dataset[choose_A1]==choose_A2]

    #篩選參考值
    reference_dataset = dataset.copy()
    reference_dataset = dataset.loc[dataset[choose_B1]==choose_B2]


    for i, feature in enumerate(features, start=1):
        fig.add_trace(go.Indicator(
            domain={'x': [0.2, 0.8], 'y': [0, 1]},
            value=filtered_dataset[feature].mean(),
            mode="gauge+number+delta",
            delta={'reference': reference_dataset[feature].mean()},
            gauge={'axis': {'range': Range},
                   'steps': [
                       {'range': [Range[0], reference_dataset[feature].mean()], 'color': "lightgray"},
                       {'range': [reference_dataset[feature].mean(), Range[1]], 'color': "#FFFFFF"}],
                   'shape': "bullet",
                   'bar': {'thickness': 0.2, 'color': "#EB4537"},
                  }
        ), row=i, col=1)

    fig.update_layout(
        width=width,
        height=height * rows,  # 調整高度(根據子圖數)
        showlegend=False
    )

    st.plotly_chart(fig)

# 過濾函數


# 調用函數
option_5 = st.selectbox("",
   ('性別', '學院', '年級', '年齡', '戶籍地', '在意身邊的朋友親中嗎?',
    '在意伴侶親中嗎?', '民族認同', '家庭慣用語言', '朋友親中比例', '兩岸關係', '是否贊成和民主化後中國統一',
    '認為選舉最重要的是?', '參與候選人或政黨活動', '是否勸說他人支持特定候選人', '是否認為意識型態長期凌駕於內政問題？',
    '2024總統投給誰', '2024不分區投給哪個政黨'),
   index=None,
   placeholder="請選擇要分析的要素...",
   key="option_5"
)
if choose_dic.get(option_5) is not None :
    group_names = list(dataset.groupby(choose_dic.get(option_5)).groups.keys())
    option_6 = st.selectbox("",
    group_names,
    index=None,
    placeholder="請選擇要分析的類別...",
    key="option_6"
    )
    st.write("You selected:", option_5,option_6)
option_7 = st.selectbox("",
   ('性別', '學院', '年級', '年齡', '戶籍地', '在意身邊的朋友親中嗎?',
    '在意伴侶親中嗎?', '民族認同', '家庭慣用語言', '朋友親中比例', '兩岸關係', '是否贊成和民主化後中國統一',
    '認為選舉最重要的是?', '參與候選人或政黨活動', '是否勸說他人支持特定候選人', '是否認為意識型態長期凌駕於內政問題？',
    '2024總統投給誰', '2024不分區投給哪個政黨'),
   index=None,
   placeholder="請選擇要分析的要素...",
   key="option_7"
)
if choose_dic.get(option_7) is not None :
    group_names = list(dataset.groupby(choose_dic.get(option_7)).groups.keys())
    option_8 = st.selectbox("",
    group_names,
    index=None,
    placeholder="請選擇要分析的類別...",
    key="option_8"
    )
    st.write("You selected:", option_7,option_8)
if st.toggle("標準化"):
    if option_5 is not None and option_6 is not None and option_7 is not None and option_8 is not None:
        plot_gauge(standard_dataset,features, choose_dic.get(option_5),option_6,choose_dic.get(option_7),option_8,Range=[-3,3])
    else:
        st.info("請選擇有效的索引。")
else :
    if option_5 is not None and option_6 is not None and option_7 is not None and option_8 is not None:
        plot_gauge(dataset,features, choose_dic.get(option_5),option_6,choose_dic.get(option_7),option_8,Range=[0,7])
    else:
        st.info("請選擇有效的索引。")
