import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados 
df = pd.read_csv("dados_logistica.csv")

# Título
st.title("Dashboard de Logística")

# Exibir tabela 
st.dataframe(df)

# KPIs principais
total_pedidos = df["Pedido_ID"].nunique()
valor_total = df["Valor_Total"].sum()
pct_no_prazo = (df[df["Status_Entrega"] == "Entregue"].shape[0] / total_pedidos) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Pedidos Totais", total_pedidos)
col2.metric("Valor Total (R$)", f"{valor_total:,.2f}")
col3.metric("Entregas no Prazo (%)", f"{pct_no_prazo:.1f}%")

# Filtros na barra lateral
st.sidebar.header("Filtros")

# Filtro por transportadora
transportadora = st.sidebar.selectbox(
    "Transportadora",
    ["Todas"] + df["Transportadora"].unique().tolist()
)

# Filtro por status de entrega
status = st.sidebar.multiselect(
    "Status da Entrega",
    df["Status_Entrega"].unique().tolist(),
    default=df["Status_Entrega"].unique().tolist()
)

# Aplicar filtros
df_filtrado = df.copy()
if transportadora != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Transportadora"] == transportadora]
df_filtrado = df_filtrado[df_filtrado["Status_Entrega"].isin(status)]

# Gráfico de pedidos por transportadora
vc = df_filtrado["Transportadora"].value_counts().reset_index()
vc.columns = ["Transportadora", "Qtd_Pedidos"]

fig1 = px.bar(
    vc,
    x="Transportadora",
    y="Qtd_Pedidos",
    labels={"Transportadora": "Transportadora", "Qtd_Pedidos": "Qtd. Pedidos"},
    title="Pedidos por Transportadora"
)
st.plotly_chart(fig1)

# Gráfico de status de entrega
fig2 = px.pie(
    df_filtrado,
    names="Status_Entrega",
    title="Status das Entregas",
    hole=0.4
)
st.plotly_chart(fig2)
