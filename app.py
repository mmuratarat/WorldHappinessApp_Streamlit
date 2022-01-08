import pandas as pd
import plotly_express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title="Dünya Mutluluk Raporu 2021", page_icon=":smile:", layout="wide")

st.title("Dünya Mutluluk Raporu Analitiği")
st.markdown("Hoş geldiniz! Aramanızı daraltmak için lütfen ekranınızın solunda bulunan kenar çubuğundaki filtrelerden seçim yapınız.")
st.markdown("##")
data = pd.read_csv(filepath_or_buffer = "world-happiness-report-2021.csv")

# Ortanca Merdiven Skoru
median_ladderScore = np.median(data['Ladder score'])
howMany_Ladders = "\U0001fa9c" * int(median_ladderScore)
# Ortalama yaşam beklentisi
mean_lifeExpectancy = np.mean(data['Healthy life expectancy'])
# En mutlu ülke
happiest_country = data[data['Ladder score'] == np.max(data['Ladder score'])]['Country name'].item()
finland_flag = ":flag-fi:"

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.markdown(body = '<p style="font-size: 20px; font-weight:bold;">Ortanca Merdiven Skoru:</p>', unsafe_allow_html=True)
    st.subheader(body=f"{median_ladderScore} {howMany_Ladders}")
with middle_column:
    st.markdown(body = '<p style="font-size: 20px; font-weight:bold;">Ortalama Yaşam Beklentisi:</p>', unsafe_allow_html=True)
    st.subheader(body =  f"{mean_lifeExpectancy: .2f} yıl")
with right_column:
    st.markdown(body = '<p style="font-size: 20px; font-weight:bold;">En Mutlu Ülke:</p>', unsafe_allow_html=True)
    st.subheader(body=f"{finland_flag} {happiest_country}")

st.markdown("---")
############### KENAR ÇUBUĞU (SIDEBAR) ###############

st.sidebar.header("Lütfen burada filtreleyin:")

# Bölge Çoklu-seçimi (Multi-selection)

st.markdown(body = '<p style="font-family:sans-serif; font-size: 24px;">Bölgelere Göre Veri Kümesi</p>', unsafe_allow_html=True)

region_selected = st.sidebar.multiselect(label = "Bölge seçiniz:",
                                         options = data['Regional indicator'].unique(),
                                         default = data['Regional indicator'].unique())

data_regions = data.query("`Regional indicator` == @region_selected")

numer_of_results = data_regions.shape[0]

st.markdown(f"*Gözlem sayısı: {numer_of_results}*")
st.dataframe(data=data_regions)


#Merdiven Skoru Kaydırıcısı (Slider)
st.markdown(body = '<p style="font-family:sans-serif; font-size: 24px;">Merdiven Skoruna Göre Veri Kümesi</p>', unsafe_allow_html=True)

score = st.sidebar.slider(label = 'Minimum Ladder Skoru Seçiniz:', min_value=5, max_value=10, value = 10) 

data_ladderScore = data[data['Ladder score'] <= score] 

numer_of_results2 = data_ladderScore.shape[0]

st.markdown(f"*Gözlem sayısı: {numer_of_results2}*")
st.dataframe(data=data_ladderScore)

st.markdown("----")

# GRAFİKLER

# Saçılım Grafiği
fig_gdp_lifeExpect = px.scatter(data_frame = data_regions,
x="Logged GDP per capita",
y="Healthy life expectancy",
size="Ladder score",
color="Regional indicator",
hover_name="Country name",
size_max=10,
title='Kişi başına GSYİH ve Yaşam Beklentisi',
template='ggplot2')

fig_gdp_lifeExpect.update_layout(
    xaxis=(dict(showgrid=False))
)


# Çubuk grafiği
fig_ladderByCountry = px.bar(data_frame= data_regions, x='Ladder score', y='Country name', orientation='h', title='Ülkeler bazında merdiven skorları', template='ggplot2')

fig_ladderByCountry.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_gdp_lifeExpect, use_container = True)
right_column.plotly_chart(fig_ladderByCountry, use_container = True)

# ---- STREAMLIT STİLİNİ SAKLA ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)