# Importação das bibliotecas necessárias
import streamlit as st  # Biblioteca para criar interfaces web interativas
import yfinance as yf  # Biblioteca para baixar dados financeiros
import numpy as np  # Biblioteca para manipulação numérica
import cvxpy as cp  # Biblioteca para resolver problemas de otimização 
import plotly.graph_objects as go  # Biblioteca para visualização interativa
import pandas as pd  # Biblioteca para manipulação de dados

# Título do aplicativo
st.title("Otimização de Portfólio de Investimentos")

# Função para retornar uma lista fixa de tickers (ativos disponíveis)
def get_tickers():
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA"]

# Função para definir os limites mínimos e máximos de alocação para cada perfil de risco
def get_risk_limits(profile):
    if profile == "Conservador":
        return 0.05, 0.3  # Limite de alocação: entre 5% e 30% por ativo
    elif profile == "Moderado":
        return 0.1, 0.4  # Limite de alocação: entre 10% e 40% por ativo
    elif profile == "Agressivo":
        return 0.15, 0.6  # Limite de alocação: entre 15% e 60% por ativo

# Função para calcular os retornos esperados dos ativos com base em dados históricos
def get_expected_returns(selected_tickers, start_date, end_date):
    # Baixa os preços ajustados de fechamento usando yfinance
    data = yf.download(selected_tickers, start=start_date, end=end_date)["Adj Close"]
    # Calcula os retornos diários a partir dos preços
    daily_returns = data.pct_change().dropna()
    # Calcula os retornos médios anuais multiplicando a média diária por 252 (dias úteis por ano)
    expected_returns = daily_returns.mean() * 252
    return expected_returns, daily_returns

# Função para otimizar o portfólio usando otimização 
def optimize_portfolio(expected_returns, min_allocation, max_allocation):
    # Número de ativos
    n_assets = len(expected_returns)
    # Define a variável de otimização: pesos (proporções alocadas em cada ativo)
    weights = cp.Variable(n_assets)
    # Define a função objetivo: maximizar o retorno esperado do portfólio
    objective = cp.Maximize(expected_returns.values @ weights)
    # Define as restrições do problema
    constraints = [
        cp.sum(weights) == 1,  # A soma dos pesos deve ser igual a 100% (1 em escala decimal)
        weights >= min_allocation,  # Cada peso deve ser maior ou igual à alocação mínima
        weights <= max_allocation  # Cada peso deve ser menor ou igual à alocação máxima
    ]
    # Cria o problema de otimização
    problem = cp.Problem(objective, constraints)
    # Resolve o problema usando o solver interno de CVXPY
    problem.solve()
    # Verifica se a solução é ótima e retorna os pesos calculados
    return weights.value if problem.status == cp.OPTIMAL else None

# Sidebar para configurar as opções do portfólio
st.sidebar.header("Configurações de Portfólio")
tickers = get_tickers()  # Lista de ativos disponíveis
# Multiseleção para escolher os ativos do portfólio
selected_tickers = st.sidebar.multiselect("Escolha os ativos para seu portfólio:", tickers)

# Seleção do perfil de risco
risk_profile = st.sidebar.selectbox("Selecione seu perfil de investidor:", ["Conservador", "Moderado", "Agressivo"])
# Obtém os limites de alocação com base no perfil de risco
min_allocation, max_allocation = get_risk_limits(risk_profile)

# Seleção do prazo de investimento
investment_period = st.sidebar.selectbox("Escolha seu prazo de investimento:", ["Curto prazo (1-3 anos)", "Médio prazo (3-7 anos)", "Longo prazo (7+ anos)"])
# Define as datas de início e fim para análise histórica com base no prazo escolhido
start_date, end_date = {
    "Curto prazo (1-3 anos)": ("2022-01-01", "2024-01-01"),
    "Médio prazo (3-7 anos)": ("2018-01-01", "2024-01-01"),
    "Longo prazo (7+ anos)": ("2015-01-01", "2024-01-01")
}[investment_period]

# Verifica se ao menos um ativo foi selecionado
if selected_tickers:
    st.write(f"### Ativos Selecionados: {', '.join(selected_tickers)}")
    st.write(f"Perfil de Risco: {risk_profile}")
    
    # Calcula os retornos esperados e retornos diários
    expected_returns, daily_returns = get_expected_returns(selected_tickers, start_date, end_date)
    
    # Otimiza o portfólio para encontrar a alocação ideal
    optimal_weights = optimize_portfolio(expected_returns, min_allocation, max_allocation)
    
    # Verifica se a solução foi encontrada
    if optimal_weights is not None:
        # Exibe a alocação ideal
        allocation = pd.DataFrame({
            "Ativo": selected_tickers,
            "Alocação Ideal (%)": [round(weight * 100, 2) for weight in optimal_weights]
        })
        st.write("### Alocações Ideais do Portfólio")
        st.dataframe(allocation)

        # Cria um gráfico de pizza para a distribuição do portfólio
        fig = go.Figure(data=[go.Pie(labels=allocation["Ativo"], values=allocation["Alocação Ideal (%)"])])
        fig.update_layout(title="Distribuição Ideal do Portfólio")
        st.plotly_chart(fig)

        # Exibe os preços históricos acumulados dos ativos selecionados
        st.write("### Preços Históricos dos Ativos Selecionados")
        st.line_chart(daily_returns.cumsum() + 1)

        # Calcula o retorno esperado do portfólio otimizado
        expected_portfolio_return = (expected_returns.values @ optimal_weights) * 100
        st.write(f"Retorno esperado do portfólio otimizado: **{expected_portfolio_return:.2f}% ao ano**")
    else:
        st.error("A otimização falhou. Tente aumentar o número de ativos selecionados ou alterar o perfil de risco.")
else:
    st.warning("Por favor, selecione ao menos um ativo para começar a otimização.")
