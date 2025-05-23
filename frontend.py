import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Nomi Piacenza", layout="wide", page_icon="👶", initial_sidebar_state="expanded")

st.markdown("""
<style>
body, .stApp { background-color: #f7f6f2; }
[data-testid="stSidebar"] { background-color: #e7e6e1; }
.stButton>button { background-color: #b5d0e6; color: #333; border-radius: 8px; }
.stDataFrame, .stTable { background-color: #fff8f0; }
</style>
""", unsafe_allow_html=True)

st.title("👶 Analisi Nomi Comune di Piacenza")

# Sidebar filters
st.sidebar.header("Filtri")
nome = st.sidebar.text_input("Nome contiene")
cittadinanza = st.sidebar.selectbox("Cittadinanza", ["", "Italiani", "Stranieri"])
sesso = st.sidebar.selectbox("Sesso", ["", "M", "F"])
anno_min, anno_max = st.sidebar.slider("Anno di nascita", 1987, 2025, (2015, 2025))
sort_by = st.sidebar.selectbox("Ordina per", ["Occorrenze", "Anno Nascita", "Nome", "Cittadinanza", "Sesso"])
sort_order = st.sidebar.radio("Ordine", ["desc", "asc"])

# Data fetch
params = {
    "nome": nome or None,
    "cittadinanza": cittadinanza or None,
    "sesso": sesso or None,
    "anno_min": anno_min,
    "anno_max": anno_max,
    "sort_by": sort_by,
    "sort_order": sort_order
}
res = requests.get(f"{API_URL}/names", params=params)
data = pd.DataFrame(res.json()) if res.ok else pd.DataFrame()

st.subheader("Tabella dati filtrati")
st.dataframe(data, use_container_width=True)

# Grafici
st.subheader("Visualizzazione grafica")
graph_type = st.radio("Tipo di grafico", ["Istogramma", "Torta"])
agg_by = st.selectbox("Aggrega per", ["Nome", "Cittadinanza", "Sesso", "Anno Nascita"])

# Aggregazione sui dati filtrati
if not data.empty:
    agg_data = data.groupby(agg_by)["Occorrenze"].sum().reset_index()
    agg_data = agg_data.sort_values(by="Occorrenze", ascending=False)
    if not agg_data.empty:
        if graph_type == "Istogramma":
            fig = px.bar(
                agg_data.head(20),
                x=agg_by,
                y="Occorrenze",
                color=agg_by,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.pie(
                agg_data.head(10),
                names=agg_by,
                values="Occorrenze",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nessun dato da visualizzare per questi filtri.")
else:
    st.info("Nessun dato da visualizzare per questi filtri.")
