import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# Configurações do Dashboard
st.set_page_config(page_title="Dashboard de Análise", page_icon="icons8-analytics-48.png", layout="wide")

st.markdown(f"""
<div style="text-align: center;">
    <span style="font-size: 35px; font-weight: bold;">Dashboard de Análise de Receitas</span><br>
</div>
""", unsafe_allow_html=True)

# Linha Divisória
st.markdown("<hr style='border: 1px solid #00FF00; margin: 20px 0;'>",
            unsafe_allow_html=True)

# Função de Carregamento de Dados
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("Erro: Arquivo 'commercial_data.csv' não encontrado.")
        st.stop()
    return df

# Carregar os dados
file_path = "commercial_data.csv"
df = load_data(file_path)

# Verificar as colunas necessárias
required_columns = ["Customer_ID", "Region", "Total_Revenue", "Quantity", "Cost"]
if not all(col in df.columns for col in required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    st.error(f"Erro: As seguintes colunas estão ausentes: {', '.join(missing_columns)}")
    st.stop()

# Menu Lateral
st.sidebar.image("logo1.png", caption="Online Analytics")
menu = st.sidebar.radio("Selecione a visualização:", ["Visão Geral", "Tabela de Dados", "Gráficos"])

# Filtros Dinâmicos
st.sidebar.title("Filtros")
selected_region = st.sidebar.multiselect("Selecione a(s) Região(ões):", options=df["Region"].unique(), default=df["Region"].unique())
min_revenue, max_revenue = st.sidebar.slider("Intervalo de Receita Total:", min_value=int(df["Total_Revenue"].min()), max_value=int(df["Total_Revenue"].max()), value=(int(df["Total_Revenue"].min()), int(df["Total_Revenue"].max())))

# Aplicar Filtros
filtered_data = df[(df["Region"].isin(selected_region)) & df["Total_Revenue"].between(min_revenue, max_revenue)]

# Exibição dos Dados
if filtered_data.empty:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
    
else:
    # Menu: Visão Geral
    if menu == "Visão Geral":
        st.markdown(f"""
    <div style="text-align: center;">
        <span style="font-size: 25px; font-weight: bold;">Visão Geral das Métricas</span><br>
    </div>
    """, unsafe_allow_html=True)

        # Calcular Métricas
        total_revenue = filtered_data["Total_Revenue"].sum()
        avg_quantity = filtered_data["Quantity"].mean()
        total_cost = filtered_data["Cost"].sum()
        net_revenue = total_revenue - total_cost
        avg_ticket = total_revenue / \
            filtered_data["Quantity"].sum(
            ) if filtered_data["Quantity"].sum() > 0 else 0

        # Linha Divisória
        st.markdown(
            "<hr style='border: 5px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)

        # Exibir Métricas
        st.markdown(f"""
    <div style="text-align: left;">
        <span style="font-size: 20px; font-weight: bold;">Principais Métricas</span><br>
    </div><br>
    """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5, gap='large')
        with col1:
            st.image("negocios-e-financas.png", width=32)
            st.markdown(f"""
    <div style="text-align: center;">
        <span style="font-size: 15px; font-weight: bold;">Receita Total</span><br>
        <span style="font-size: 25px; color: gray;">${total_revenue:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

        with col2:
            st.image("quantidade.png", width=32)
            st.markdown(f"""
    <div style="text-align: center;">
    <span style="font-size: 15px; font-weight: bold;">Quantidade Média</span><br>
    <span style="font-size: 25px; color: gray;">{avg_quantity:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

        with col3:
            st.image("despesas.png", width=32)
            st.markdown(f"""
    <div style="text-align: center;">
    <span style="font-size: 15px; font-weight: bold;">Custo Total</span><br>
    <span style="font-size: 25px; color: gray;">${total_cost:,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

        with col4:
            st.image("moeda-de-dolar.png", width=32)
            st.markdown(f"""
    <div style="text-align: center;">
    <span style="font-size: 15px; font-weight: bold;">Ticket Médio</span><br>
    <span style="font-size: 25px; color: gray;">${avg_ticket:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

        with col5:
            st.image("lucro-liquido_2.png", width=32)
            st.markdown(f"""
    <div style="text-align: center;">
    <span style="font-size: 15px; font-weight: bold;">Receita Líquida</span><br>
    <span style="font-size: 25px; color: gray;">${net_revenue:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)
            
        # Linha Divisória
        st.markdown(
            "<hr style='border: 5px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Gráficos Lado a Lado
col1, col2 = st.columns(2)
with col1:
    st.subheader("Receita por Região")
    revenue_by_region = (
        filtered_data.groupby("Region")["Total_Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Total_Revenue", ascending=False)
    )
    fig_bar = px.bar(
        revenue_by_region,
        x='Region',
        y='Total_Revenue',
        text='Total_Revenue',
        title="Receita por Região (Ordenada por Ranking)",
        color='Region'
    )
    # Ajustar o template do texto e o espaçamento entre as barras
    fig_bar.update_traces(
        texttemplate='<b>$%{text:,.2f}</b>',  # Formato do rótulo
        textposition='outside'        # Posição do rótulo
    )
    fig_bar.update_layout(
        bargap=0.2,  # Reduzir o espaço entre as barras
        bargroupgap=0.1,  # Ajustar espaço entre grupos (se houver)
        yaxis_title="Receita Total",
        xaxis_title="Região",
        uniformtext_minsize=10,  # Tamanho mínimo do texto uniforme
        uniformtext_mode='hide',  # Ocultar textos que não cabem
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Quantidade vs Receita")
        fig_scatter = px.scatter(
            filtered_data,
            x='Quantity',
            y='Total_Revenue',
            color='Region',
            size='Total_Revenue',
            title="Quantidade vs Receita",
            hover_name='Region'
        )
        fig_scatter.update_layout(
            yaxis_title="Receita Total", xaxis_title="Quantidade")
        st.plotly_chart(fig_scatter, use_container_width=True)

# Linha Divisória
st.markdown("<hr style='border: 1px solid #ccc; margin: 20px 0;'>",
            unsafe_allow_html=True)

# Verificar se as colunas necessárias existem
if {"Category", "Total_Revenue", "Cost"}.issubset(df.columns):
    st.header("Receita Líquida vs Receita Bruta por Categoria")

    # Calcular a Receita Líquida
    df["Net_Revenue"] = df["Total_Revenue"] - df["Cost"]

    # Agrupar os dados por categoria e calcular a soma das receitas líquidas e brutas
    revenue_by_category = df.groupby("Category")[["Net_Revenue", "Total_Revenue"]].sum().reset_index()

    # Transformar os dados para formato longo (long format) para usar no gráfico
    revenue_long = revenue_by_category.melt(
        id_vars="Category", 
        value_vars=["Net_Revenue", "Total_Revenue"],
        var_name="Revenue_Type", 
        value_name="Amount"
    )

    # Criar o gráfico de barras agrupadas
    fig = px.bar(
        revenue_long,
        x="Category",
        y="Amount",
        color="Revenue_Type",
        barmode="group",
        title="Receita Líquida vs Receita Bruta por Categoria",
        labels={"Category": "Categoria", "Amount": "Valor", "Revenue_Type": "Tipo de Receita"}
    )

    # Personalizar o layout com maior espaçamento
    fig.update_layout(
        xaxis_title="Categoria",
        yaxis_title="Valor da Receita",
        legend_title="Tipo de Receita",
        bargap=0.2,  # Aumentar o espaço entre os grupos de barras
        xaxis_tickangle=-45,  # Ajustar a rotação dos rótulos do eixo X para melhor visibilidade
        xaxis={'categoryorder':'total descending'},  # Ordenar categorias por total
    )

    # Adicionar rótulos de dados acima das barras com negrito e fonte 14, em dólar
    fig.update_traces(
        texttemplate='$ %{y:,.2f}',  
        textposition='outside',  # Rótulo acima da barra
        textfont=dict(size=16, family="Arial, sans-serif", color="black", weight="bold"),
        insidetextanchor="start",  # Ajustar o posicionamento dos rótulos
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("O arquivo CSV não contém as colunas 'Category', 'Total_Revenue' e 'Cost'.")

    # Linha Divisória
st.markdown("<hr style='border: 5px solid #ccc; margin: 20px 10;'>",unsafe_allow_html=True)

    # Gráficos
if menu == "Gráficos":
    col1, col2 = st.columns(2)

    # Gráfico 1: Distribuição de Receita por Região
    with col1:
        st.subheader("Distribuição de Receita por Região")
        revenue_by_region = (
            filtered_data.groupby("Region")["Total_Revenue"]
            .sum()
            .reset_index()
        )
        fig_pie = px.pie(
            revenue_by_region,
            names='Region',
            values='Total_Revenue',
            title="Distribuição de Receita por Região"
        )
    
        # Formatando o texto em negrito e ajustando os rótulos
        fig_pie.update_traces(textinfo='percent+label', textfont=dict(size=10,
                        family="Arial, sans-serif", color="black", weight="bold"))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico 2: Quantidade de Clientes por Região
    with col2:
        st.subheader("Quantidade de Clientes por Região")
        customers_by_region = (
            filtered_data.groupby("Region")["Customer_ID"]
            .nunique()
            .reset_index()
            .rename(columns={"Customer_ID": "Customer_Count"})
        )
        fig_customers = px.bar(
            customers_by_region,
            x="Region",
            y="Customer_Count",
            text="Customer_Count",
            title="Quantidade de Clientes por Região",
            color="Region"
        )
        # Ajustando o texto para negrito e o espaço entre barras e rótulos
        fig_customers.update_traces(
            texttemplate='<b>%{text}</b>',  # Texto em negrito
            textposition='outside',        # Posição do rótulo
            textfont=dict(size=10, family="Arial, sans-serif",
                        color="black", weight="bold")
        )
        fig_customers.update_layout(
            bargap=0.15,  # Ajusta o espaço entre as barras
            bargroupgap=0.1,  # Ajusta o espaço entre grupos de barras
            yaxis_title="Quantidade de Clientes",
            xaxis_title="Região",
            uniformtext_minsize=10,  # Tamanho mínimo do texto
            uniformtext_mode='hide'  # Ocultar textos que não cabem
        )
        st.plotly_chart(fig_customers, use_container_width=True)

    # Linha Divisória
    st.markdown(
        "<hr style='border: 5px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)

# Tabela de Dados
if menu == "Tabela de Dados":
    st.header("Tabela de Dados")
    file_path = "commercial_data.csv"  # Carregar os dados do arquivo CSV

    try:
        # Ler o arquivo CSV
        filtered_data = pd.read_csv(file_path)

        # Agrupar os dados para sumarização
        grouped_table = (
            filtered_data.groupby("Category")
            .agg({
                "Product_Name": "count",       # Número de produtos
                "Region": "nunique",           # Regiões únicas
                "Quantity": "sum",             # Quantidade total
                "Total_Revenue": "sum",        # Receita total
            })
            .reset_index()
        )

        # Renomear as colunas
        grouped_table.rename(
            columns={
                "Category": "CATEGORIA",
                "Product_Name": "PRODUTOS VENDIDOS",
                "Region": "REGIÕES",
                "Quantity": "QUANTIDADE VENDIDA",
                "Total_Revenue": "VALOR TOTAL",
            },
            inplace=True
        )

        # Formatar as colunas de valores diretamente no DataFrame
        grouped_table["VALOR TOTAL"] = grouped_table["VALOR TOTAL"].apply(
            lambda x: f"${x:,.2f}"
        )
        grouped_table["QUANTIDADE VENDIDA"] = grouped_table["QUANTIDADE VENDIDA"].apply(
            lambda x: f"{x:,}"
        )
        grouped_table["PRODUTOS VENDIDOS"] = grouped_table["PRODUTOS VENDIDOS"].apply(
            lambda x: f"{x:,}"
        )

        # Configurar o AgGrid com filtros interativos
        gb = GridOptionsBuilder.from_dataframe(grouped_table)
        gb.configure_pagination(paginationPageSize=10)  # Paginação
        gb.configure_grid_options(domLayout='normal')  # Layout padrão
        gb.configure_default_column(
            editable=True, filter=True, sortable=True)  # Ativar filtros
        grid_options = gb.build()

        # Exibir a tabela no Streamlit com filtros interativos
        st.subheader("Tabela Interativa - Resumo por Categoria")
        response = AgGrid(
            grouped_table,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            theme="alpine",  # Temas: "alpine", "streamlit", "dark", etc.
            fit_columns_on_grid_load=True
        )


    except FileNotFoundError:
        st.error(
            f"O arquivo '{file_path}' não foi encontrado. Por favor, verifique o caminho e tente novamente.")
    except pd.errors.EmptyDataError:
        st.error(
            f"O arquivo '{file_path}' está vazio. Por favor, forneça um arquivo válido.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

        # Linha Divisória
        st.markdown(
            "<hr style='border: 5px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)
    if menu == "Gráficos":                
        st.subheader("Tabela de Dados Filtrados")
        st.write(filtered_data)



