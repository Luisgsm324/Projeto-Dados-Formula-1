# Projeto teste de Extração de Dados da Fórmula 1

O projeto foi realizado com o objetivo de extrair os dados das playlists do canal do YouTube da "Fórmula 1" a fim de se obter as corridas que obteram o maior número de visualizações no ano específico, fato que nos parâmetros determinados consideraria a corrida mais popular ocorrida nesse período. Os anos são 2021, 2022 e 2023 com um total de mais de 60 corridas ocorridas durante esses 3 anos. 

## Pré-requisitos e Execução

É necessário que se tenha a linguagem de programação *Python* instalado em sua máquina e que sejam baixado as seguintes dependências por meio dos seguintes passos:

```bash 
pip install pandas
```

```bash 
pip install --upgrade google-api-python-client
```

Por fim, para a execução do programa, basta executar o seguinte comando:

```bash 
python main.py
```

## Ferramentas e Tecnologias utilizadas

Os recursos abaixos foram utilizados com o propósito de alcançar o objetivo pretendido:

*[YouTube API](https://developers.google.com/youtube/v3?hl=pt-br) - API do YouTube utilizada para extrair os dados das playlists do canal da "Fórmula 1".

*[Statistics](https://docs.python.org/pt-br/dev/library/statistics.html) - Biblioteca do Python utilizada para os valores das Medidas Centrais.

*[Pandas](https://pandas.pydata.org/docs/) - Biblioteca do Python utilizada para organizar as informações em um formato de tabela para a melhor visualização.
