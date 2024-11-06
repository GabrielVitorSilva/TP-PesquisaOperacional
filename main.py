import streamlit as st
import yfinance as yf
import numpy as np
import cvxpy as cp
import plotly.graph_objects as go
import pandas as pd

st.title("Otimização de Portfólio de Investimentos")

def get_tickers():
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA"]

def get_risk_limits(profile):
    if profile == "Conservador":
        return 0.05, 0.3  # Aumentei o máximo para 30% para o perfil conservador
    elif profile == "Moderado":
        return 0.1, 0.4
    elif profile == "Agressivo":
        return 0.15, 0.6

def get_expected_returns(selected_tickers, start_date, end_date):
    data = yf.download(selected_tickers, start=start_date, end=end_date)["Adj Close"]
    daily_returns = data.pct_change().dropna()
    expected_returns = daily_returns.mean() * 252  # 252 dias úteis no ano
    return expected_returns, daily_returns

def optimize_portfolio(expected_returns, min_allocation, max_allocation):
    n_assets = len(expected_returns)
    weights = cp.Variable(n_assets)
    objective = cp.Maximize(expected_returns.values @ weights)
    constraints = [
        cp.sum(weights) == 1,
        weights >= min_allocation,
        weights <= max_allocation
    ]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    return weights.value if problem.status == cp.OPTIMAL else None

st.sidebar.header("Configurações de Portfólio")
tickers = get_tickers()
selected_tickers = st.sidebar.multiselect("Escolha os ativos para seu portfólio:", tickers)

risk_profile = st.sidebar.selectbox("Selecione seu perfil de investidor:", ["Conservador", "Moderado", "Agressivo"])
min_allocation, max_allocation = get_risk_limits(risk_profile)

investment_period = st.sidebar.selectbox("Escolha seu prazo de investimento:", ["Curto prazo (1-3 anos)", "Médio prazo (3-7 anos)", "Longo prazo (7+ anos)"])
start_date, end_date = {
    "Curto prazo (1-3 anos)": ("2022-01-01", "2024-01-01"),
    "Médio prazo (3-7 anos)": ("2018-01-01", "2024-01-01"),
    "Longo prazo (7+ anos)": ("2015-01-01", "2024-01-01")
}[investment_period]

if selected_tickers:
    st.write(f"### Ativos Selecionados: {', '.join(selected_tickers)}")
    st.write(f"Perfil de Risco: {risk_profile}")
    
    expected_returns, daily_returns = get_expected_returns(selected_tickers, start_date, end_date)
    
    optimal_weights = optimize_portfolio(expected_returns, min_allocation, max_allocation)
    
    if optimal_weights is not None:
        allocation = pd.DataFrame({
            "Ativo": selected_tickers,
            "Alocação Ideal (%)": [round(weight * 100, 2) for weight in optimal_weights]
        })
        st.write("### Alocações Ideais do Portfólio")
        st.dataframe(allocation)

        fig = go.Figure(data=[go.Pie(labels=allocation["Ativo"], values=allocation["Alocação Ideal (%)"])])
        fig.update_layout(title="Distribuição Ideal do Portfólio")
        st.plotly_chart(fig)

        st.write("### Preços Históricos dos Ativos Selecionados")
        st.line_chart(daily_returns.cumsum() + 1)

        expected_portfolio_return = (expected_returns.values @ optimal_weights) * 100
        st.write(f"Retorno esperado do portfólio otimizado: **{expected_portfolio_return:.2f}% ao ano**")
    else:
        st.error("A otimização falhou. Tente aumentar o número de ativos selecionados ou alterar o perfil de risco.")
else:
    st.warning("Por favor, selecione ao menos um ativo para começar a otimização.")
