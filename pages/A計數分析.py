import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
st.set_page_config(page_title="政知道了",page_icon=":bar_chart:")
choose_dic={
    '性別':'gender','學院':'college','年級':'grade','年齡':'age',
    '戶籍地':'residence','在意身邊的朋友親中嗎?':'friend_pro_china','在意伴侶親中嗎?':'marriage_pro_china',
    '民族認同':'self_identity','家庭慣用語言':'family_language','朋友親中比例':'friend_pro_china_ratio',
    '兩岸關係':'taiwan_china_relation','是否贊成和民主化後中國統一':'support_unification_if_democratic',
    '認為選舉最重要的是?':'most_important_democracy_aspect','參與候選人或政黨活動頻率':'election_volunteer',
    '是否勸說他人支持特定候選人':'election_persuasion','是否認為意識型態長期凌駕於內政問題？':'ideology_over_domestic_issues',
    '2024總統投給誰':'candidate_voted_for','2024不分區投給哪個政黨':'party_supported'
}
features = ['us_relation_opinion', 'china_relation_opinion',
            'international_alignment_opinion', 'china_democracy_destruction_opinion',
            'taiwan_improvement_opinion', 'taiwan_political_fighting_opinion',
            'democracy_satisfaction', 'future_democracy_prospects']
dataset = pd.read_csv('datas.csv')
sc = StandardScaler()
standard =sc.fit_transform(dataset[features])
standard_data = pd.DataFrame(standard, columns=features)
standard_dataset = pd.concat([dataset.drop(columns=features), standard_data], axis=1)

st.subheader('旭日圖')

# 旭日圖
def plot_sunburst(dataset, feature1, feature2):
    if feature1 is None or feature2 is None:
        st.warning("請選擇有效的索引。")
        return
    # 計數資料
    data_counts = dataset.groupby([feature1, feature2]).size().reset_index(name='count')
    # 計算總數
    total_count = data_counts['count'].sum()
    
    # 計算每一組的百分比
    data_counts['percentage'] = data_counts['count'] / total_count * 100
    
    # 繪製 sunburst 圖表，並顯示百分比
    fig = px.sunburst(
        data_counts,
        path=[feature1, feature2],
        values='count',
        custom_data=['percentage'],
    )
    # 更新 hover 顯示百分比
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{customdata[0]:.2f}%'
    )
    st.plotly_chart(fig)


# 調用函數
choose_dic={
    '性別':'gender','學院':'college','年級':'grade','年齡':'age',
    '戶籍地':'residence','在意身邊的朋友親中嗎?':'friend_pro_china','在意伴侶親中嗎?':'marriage_pro_china',
    '民族認同':'self_identity','家庭慣用語言':'family_language','朋友親中比例':'friend_pro_china_ratio',
    '兩岸關係':'taiwan_china_relation','是否贊成和民主化後中國統一':'support_unification_if_democratic',
    '認為選舉最重要的是?':'most_important_democracy_aspect','參與候選人或政黨活動頻率':'election_volunteer',
    '是否勸說他人支持特定候選人':'election_persuasion','是否認為意識型態長期凌駕於內政問題？':'ideology_over_domestic_issues',
    '2024總統投給誰':'candidate_voted_for','2024不分區投給哪個政黨':'party_supported'
}
option_1 = st.selectbox("",
   ('性別', '學院', '年級', '年齡', '戶籍地', '在意身邊的朋友親中嗎?',
    '在意伴侶親中嗎?', '民族認同', '家庭慣用語言', '朋友親中比例', '兩岸關係', '是否贊成和民主化後中國統一',
    '認為選舉最重要的是?', '參與候選人或政黨活動', '是否勸說他人支持特定候選人', '是否認為意識型態長期凌駕於內政問題？',
    '2024總統投給誰', '2024不分區投給哪個政黨'),
   index=None,
   placeholder="請選擇要分析的主要要素...",
   key="option_1"
)
option_2 = st.selectbox("",
   ('性別', '學院', '年級', '年齡', '戶籍地', '在意身邊的朋友親中嗎?',
    '在意伴侶親中嗎?', '民族認同', '家庭慣用語言', '朋友親中比例', '兩岸關係', '是否贊成和民主化後中國統一',
    '認為選舉最重要的是?', '參與候選人或政黨活動', '是否勸說他人支持特定候選人', '是否認為意識型態長期凌駕於內政問題？',
    '2024總統投給誰', '2024不分區投給哪個政黨'),
   index=None,
   placeholder="請選擇要分析的次要要素...",
   key="option_2"
)
st.write("當前選擇:", option_1,"裡的",option_2)
if option_1 is not None and option_2 is not None and option_1!=option_2:
    plot_sunburst(dataset, choose_dic.get(option_1), choose_dic.get(option_2))
else:
    st.info("請選擇有效的索引。")

st.divider() 
st.subheader('瀑布圖')
element = pd.DataFrame()
labs={v: k for k, v in choose_dic.items()}
# 迭代选项，添加被选中的列
with st.expander("點擊展開要素清單"):
    for select in choose_dic:
        if st.checkbox(select):
            element = pd.concat([element, dataset[[choose_dic.get(select)]]], axis=1)
# 检查是否有选中的列
if not element.empty:
    fig = px.parallel_categories(element,labels=labs)
    st.plotly_chart(fig)
else:
    st.info("請至少選擇一個選項")
