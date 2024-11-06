Documentação Completa do Sistema de Otimização de Portfólio de Investimentos: 
### Sumário
1. Introdução
2. Bibliotecas Necessárias
3. Descrição do Código Passo a Passo
4. Como Executar o Projeto
5. Resultados Esperados
6. Referências
1. Introdução
Este documento detalha o funcionamento de um sistema de otimização de portfólio de
investimentos. O sistema foi desenvolvido utilizando a linguagem Python e várias bibliotecas
importantes para a análise e visualização dos dados financeiros. O principal objetivo do sistema é
ajudar os investidores a decidir como distribuir seus recursos em diferentes ativos de forma
otimizada, maximizando o retorno esperado, mas respeitando um nível de risco conforme o perfil do
investidor. O código utiliza otimização linear para encontrar a alocação ideal dos recursos.
2. Bibliotecas Necessárias
Para executar o projeto, as seguintes bibliotecas devem ser instaladas:
pip install streamlit yfinance numpy cvxpy plotly pandas
Essas bibliotecas são essenciais para o funcionamento do projeto e têm as seguintes funções:
- **streamlit**: Facilita a criação de interfaces de usuário interativas para a aplicação web.
- **yfinance**: Usada para obter os dados financeiros de ativos como ações e títulos.
- **numpy**: Realiza cálculos numéricos para trabalhar com arrays e álgebra linear.
- **cvxpy**: Resolve problemas de otimização, como o cálculo da alocação ótima de ativos.
- **plotly**: Cria gráficos interativos que ajudam a visualizar os resultados de forma clara.
- **pandas**: Manipula os dados financeiros, como a organização e preparação das séries
temporais de preços.
3. Descrição do Código Passo a Passo
### Passo 1: Importação das Bibliotecas
O código começa com a importação das bibliotecas necessárias para o processamento dos dados
e execução do modelo de otimização. As bibliotecas essenciais para esse processo são `streamlit`,
`yfinance`, `numpy`, `cvxpy`, `plotly` e `pandas`.
### Passo 2: Definindo os Ativos
Uma função chamada `get_tickers()` define os ativos que podem ser escolhidos pelo usuário, como
ações de empresas populares (ex.: 'AAPL', 'GOOGL'). Esses ativos representam os itens no
portfólio que serão analisados. O usuário pode selecionar os ativos com os quais deseja trabalhar.
### Passo 3: Coletando Dados Financeiros
A função `get_expected_returns()` é responsável por buscar os dados históricos dos ativos
selecionados. Ela usa a API do Yahoo Finance (`yfinance`) para pegar os preços ajustados e
calcula o retorno diário de cada ativo. Esses retornos são multiplicados por 252 (o número de dias
úteis no mercado financeiro) para estimar o retorno anualizado.
### Passo 4: Definindo os Limites de Risco
A função `get_risk_limits()` define os limites de alocação de ativos conforme o perfil de risco do
investidor. Existem três perfis possíveis:
- Conservador: Menor risco, maior concentração em ativos seguros.
- Moderado: Equilíbrio entre risco e retorno.
- Agressivo: Maior risco, com potencial para maiores retornos.
### Passo 5: Função de Otimização de Portfólio
A função `optimize_portfolio()` é o coração do sistema. Ela usa o pacote `cvxpy` para resolver o
problema de otimização linear, que visa maximizar o retorno esperado do portfólio, sujeito a uma
série de restrições:
- A soma das alocações dos ativos deve ser 100% do capital disponível.
- Não podem haver alocações negativas (sem vendas a descoberto).
A função retorna as alocações ótimas dos ativos e o retorno esperado.
### Passo 6: Interface de Usuário com Streamlit
O `streamlit` é usado para criar uma interface web onde o usuário pode escolher os ativos, definir o
perfil de risco e visualizar os resultados de otimização em gráficos interativos. A interface inclui:
- Um painel para escolher os ativos e o perfil de risco.
- Exibição das alocações ótimas em gráficos interativos.
- O retorno esperado do portfólio com base na otimização.
4. Como Executar o Projeto
Para rodar o projeto, siga os seguintes passos:
1. Instale as bibliotecas necessárias usando o comando:
 pip install streamlit yfinance numpy cvxpy plotly pandas
2. Salve o código em um arquivo, por exemplo `main.py`.
3. No terminal, execute o comando para rodar o aplicativo Streamlit:
 streamlit run main.py
4. O navegador abrirá automaticamente a interface do usuário onde o investidor pode interagir com
o sistema.
5. Resultados Esperados
Quando o sistema é executado com os parâmetros de entrada fornecidos, o usuário verá a
alocação ótima do portfólio de acordo com os dados históricos dos ativos selecionados. O resultado
incluirá as alocações ideais para cada ativo no portfólio e o retorno esperado anualizado.
Além disso, o usuário poderá visualizar gráficos interativos, como:
- A comparação entre os ativos selecionados e seus retornos esperados.
- O gráfico do portfólio otimizado, exibindo como os recursos foram distribuídos.
- O perfil de risco escolhido e seu impacto na alocação dos ativos.
6. Referências
1. [Streamlit Documentation](https://docs.streamlit.io)
2. [cvxpy Documentation](https://www.cvxpy.org)
3. [yfinance Documentation](https://pypi.org/project/yfinance/)
4. [Plotly Documentation](https://plotly.com/python/)
5. [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
6. [Numpy Documentation](https://numpy.org/doc/stable/)
