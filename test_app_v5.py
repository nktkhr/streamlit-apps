import altair as alt
import streamlit as st
import numpy as np
import scipy as sp
import pandas as pd

st.set_page_config(layout="wide")

st.title('統計ダッシュボード')
uploaded_file = st.file_uploader("CSVファイルのアップロード", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=0)
    # 定量データ項目のリスト
    item_list = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
    
    # サイドバー
    st.sidebar.title("統計ダッシュボード")
    st.sidebar.markdown('###')
    st.sidebar.markdown("### *変数の選択*")
    item3 = st.sidebar.selectbox('ヒストグラムの変数', item_list, index=3)
    item4 = st.sidebar.selectbox('箱ひげ図の変数', item_list, index=3)
    item1 = st.sidebar.selectbox('散布図:変数1', item_list, index=0)
    item2 = st.sidebar.selectbox('散布図:変数2', item_list, index=3)
    
    source = df
    # コンテンツ
    #ベース
    base = alt.Chart(source).properties(height=300)
    #散布図
    point = base.mark_circle(size=50).encode(
    x=alt.X(item1 + ':Q', title=item1),
    y=alt.Y(item2 + ':Q', title=item2)
    )
    #ヒストグラム
    histgram = base.mark_bar(opacity=1.0).encode(
    x=alt.X(item3 + ':Q', title=item3,
    bin=alt.Bin(),
    axis=alt.Axis(labelFontSize=15, ticks=True, titleFontSize=18)),
    y=alt.Y("count()",
            axis=alt.Axis(labelFontSize=15, ticks=True, titleFontSize=18),
            stack=None
           )
    )
    #箱ひげ図
    boxplot = base.mark_boxplot(size=50, extent=0.5).encode(
        x=alt.X(item4 + ':Q', title=item4).scale(zero=False)
        
    )
    # レイアウト (コンテンツ)
    #ヒストグラム
    st.markdown('### ' + item3 + 'のヒストグラム'+'')
    st.altair_chart(histgram, use_container_width=True)
    st.markdown('### ' + item3 +'の平均値・中央値'+'')
    mean_value = source[item3].mean()
    st.write(f"{item3} の平均値は {mean_value:.2f} です。")
    median_value = source[item3].median()
    st.write(f"{item3} の中央値は {median_value:.2f} です。")
    #箱ひげ図
    st.markdown('### ' + item4 + 'の箱ひげ図'+'')
    st.altair_chart(boxplot, use_container_width=True)
    #散布図
    st.markdown('### ' + item1 + 'と' + item2 + 'の散布図'+'')
    st.altair_chart(point, use_container_width=True)
