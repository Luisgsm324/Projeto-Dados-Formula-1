# Projeto teste de Extração de Dados da Fórmula 1

O projeto, construído inteiramente por mim, foi realizado com o objetivo de extrair os dados das playlists do canal do YouTube da "Fórmula 1" a fim de se obter as corridas que obteram o maior número de visualizações no ano específico, fato que nos parâmetros determinados consideraria a corrida mais popular ocorrida nesse período. Os anos são 2021, 2022 e 2023 com um total de mais de 60 corridas ocorridas durante esses 3 anos. 

## Pré-requisitos e Execução

É necessário que se tenha a linguagem de programação *Python* instalado em sua máquina e que sejam baixado as seguintes dependências por meio dos seguintes passos:

```bash 
pip install pandas matplotlib tabulate
```

```bash 
pip install --upgrade google-api-python-client
```

Para a execução do programa, basta entrar na pasta corretamente:

```bash 
cd .\src\
```

E por fim, executar o arquivo que está localizado:

```bash 
python main.py
```

## Ferramentas e Tecnologias utilizadas

Os recursos abaixos foram utilizados com o propósito de alcançar o objetivo pretendido:

*[YouTube API](https://developers.google.com/youtube/v3?hl=pt-br) - API do YouTube utilizada para extrair os dados das playlists do canal da "Fórmula 1".

*[Statistics](https://docs.python.org/pt-br/dev/library/statistics.html) - Biblioteca do Python utilizada para os valores das Medidas Centrais.

*[Pandas](https://pandas.pydata.org/docs/) - Biblioteca do Python utilizada para organizar as informações em um formato de tabela para a melhor visualização.

*[MatplotLib](https://matplotlib.org/stable/index.html) - Biblioteca do Python utilizada para a criação do gráfico com a amostragem de certos dados.

*[Tabulate](https://pypi.org/project/tabulate/) - Biblioteca do Python utilizada para a formatação em uma melhor estrutura visual para o DataFrame criada pelo Pandas.

