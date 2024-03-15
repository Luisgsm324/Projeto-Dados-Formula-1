from googleapiclient.discovery import build
from statistics import median, mean
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from babel.numbers import format_compact_decimal, format_decimal

# A chave da API
key = "AIzaSyCls8LWBEcyvriLk4PAS5io0NJWzZYj_9Q"

youtube = build('youtube', 'v3', developerKey=key)

playlists = []

# Palavras chaves para o tratamento de dados
grand_prix_words = ["Grand Prix", "Gran Premio", "Grosser Preis", "Grossen Preis", "Grande Premio", "Grande Prêmio", "Magyar Nagydij"]
searched_years = ["2023", "2022", "2021"]

formula1_channelID = "UCB_qr75-ydFVKSF9Dmo6izg" # Id do canal da Fórmula 1 para que seja realizado a busca

next_page_token = None

"""
============================
O programa será dividido em algumas etapas:

1º Etapa: Encontrar as playlists das corridas de 2023, 2022 e 2021;
2º Etapa: Armazenar o valor das visualizações do vídeo de Highlights; 
3º Etapa: Organizar as corridas de cada ano em ordem retornando a maior e dispor os dados em um formato de tabela;
4º Etapa: Dispor os dados em formas de tabela para a permissão da visualização gráfica;
=============================
"""

# -------------- Primeira Etapa ---------------------------

# Dicionário principal que irá armazenar os dados sobre os anos.
playlists_dict = {'2021': {'playlists':[], 'totalViewYear':0, 'countRaces': 0, 'viewsList':[]}, '2022':{'playlists':[], 'totalViewYear':0,'countRaces': 0, 'viewsList':[]}, '2023':{'playlists':[], 'totalViewYear':0, 'countRaces': 0, 'viewsList':[]}}

# Variável criada com o intuito de parar de buscar mais playlists, melhorando a otimização
break_condition = False

while True:
    res = youtube.playlists().list(part='snippet', channelId=formula1_channelID, pageToken=next_page_token).execute()
    for element in res['items']:
        year_publi = element['snippet']['publishedAt'].split("-")[0]
        title = element['snippet']['title']
        if int(year_publi) >= 2021:
            for word in grand_prix_words:
                for year in searched_years:
                    if word in title and year == year_publi:
                        info_dict = {'id':None, 'title':None, 'totalViews': 0 }
                        info_dict['id'], info_dict['title'] = element['id'], title
                        playlists_dict[year_publi]['playlists'].append(info_dict)
                        playlists_dict[year_publi]['countRaces'] += 1
        # Quando o ano for menor que 2021, não tem mais necessidade de continuar a procurar em todas as playlist, então tornamos uma variável True para que se dê um break no loop
        else:
            break_condition = True
    
    if break_condition:
        break
    
    next_page_token = res.get('nextPageToken')

# -------------- Segunda Etapa ---------------------------
 
for year in playlists_dict.keys():
    for playlist in playlists_dict[year]['playlists']:
        # Essa variável foi criado com o propósito de procurar o vídeo correspondentes aos highlights da corrida (Em certas situações ele não é o primeiro elemento)
        index = 0
        res = youtube.playlistItems().list(part='snippet', maxResults=100, playlistId=playlist['id']).execute()
        videos_info = res['items']
        while True:
            # Para o nosso algoritmo, a determinação do total de Views de uma determinada corrida vai dos vídeos de highlights.
            # Existe um caso específico que o "Race highlights" não está no primeiro vídeo e por isso, cria-se um loop com a variável "index"
            # Outra situação seria que não existe um "Race highlights" e sim um "Qualifying Highlights" que foi tratado também.
            if "Race Highlights" not in videos_info[index]['snippet']['title']:
                if "Qualifying Highlights" not in videos_info[index]['snippet']['title']:
                    index += 1
                else:
                    break
            else:
                break
        
        video_id = videos_info[index]['snippet']['resourceId']['videoId']
        res = youtube.videos().list(part='statistics', id=video_id).execute()
        playlist['totalViews'] += int(res['items'][0]['statistics']['viewCount'])

        playlists_dict[year]['viewsList'].append(playlist['totalViews'])       
        playlists_dict[year]['totalViewYear'] += playlist['totalViews']      

# -------------- Terceira Etapa --------------------------- 

# Os resultados estão dispostos em um dicionário que vai armazenar as informações de médias, medianas...
# Para que seja feito a tabela com os dados apropriados.
results = {'years': [], 'medians': [], 'averages': [], 'most_watched_race': [], 'totalViewRace':[], 'totalViewPerYear': []}

# Preencher o dicionário results com as informações que foram adquiridas anteriormente e
# determinar quais foram as corridas mais assistidas em cada ano, a sua média, mediana e outros.
# Outro ponto importante focado foi a utilização de uma formatação dos dados para a melhor visualização
for year in playlists_dict:
    most_watched_race = max(playlists_dict[year]['playlists'], key=lambda x:x['totalViews'])
    results['years'].append(year)
    
    median_variable = median(playlists_dict[year]['viewsList'])
    formated_median = format_compact_decimal(median_variable, format_type='short', fraction_digits=2, locale='pt_BR')
    results['medians'].append(formated_median)

    average_variable = mean(playlists_dict[year]['viewsList'])
    formated_average = format_compact_decimal(average_variable, format_type='short',fraction_digits=2, locale='pt_BR')
    results['averages'].append(formated_average)
    
    title = most_watched_race['title'].replace("Formula 1", "")
    results['most_watched_race'].append(title)
    
    formated_totalview = format_decimal(most_watched_race['totalViews'])
    results['totalViewRace'].append(formated_totalview)
    
    formated_totalviewYear = format_decimal(playlists_dict[year]['totalViewYear'])
    results['totalViewPerYear'].append(formated_totalviewYear)

df = pd.DataFrame(results)
headers_list = ["Ano", "Mediana", "Média", "Corrida mais vista", "Views Corrida", "Views Ano Total"]
print(tabulate(df, headers=headers_list, tablefmt='grid'))

# -------------- Quarta Etapa ---------------------------
# Devido à alguns erros na criação da tabela e para melhoria da leitura, 
# criei uma função para transformar os números em float e apenas os 3 primeiros (para evitar um número tão extenso).
def format_number(results_list):
    liney = []
    for element in results_list:
        x = str(element)[0:3]
        number = float(x)
        liney.append(number)
    return liney

liney = format_number(results['totalViewPerYear'])
plt.bar(results['years'], liney, label='Total de Views por ano (Em milhões)')

plt.legend()
plt.show()