"""
{09/03/2024} -> 
Primeiro teste para conseguir os ID's da playlist.
"""
from googleapiclient.discovery import build
from statistics import median, mean
import pandas as pd


# A chave da API
key = "AIzaSyCls8LWBEcyvriLk4PAS5io0NJWzZYj_9Q"

youtube = build('youtube', 'v3', developerKey=key)

playlists = []
grand_prix_words = ["Grand Prix", "Gran Premio", "Grosser Preis", "Grossen Preis", "Grande Premio", "Grande Prêmio", "Magyar Nagydij"]

searched_years = ["2023", "2022", "2021"]
formula1_channelID = "UCB_qr75-ydFVKSF9Dmo6izg"
next_page_token = None

"""
============================
O programa será dividido em algumas etapas:

1º Etapa: Encontrar as playlists das corridas de 2023, 2022 e 2021;
2º Etapa: Realizar o somatório dos vídeos em cada playlist; 
3º Etapa: Organizar as corridas de cada ano em ordem retornando a maior;
4º Etapa: Dispor os dados de uma forma acessível e tranquila (utilizar bibliotecas externas para executar esses trabalhos);
=============================

"""

# -------------- Primeira Etapa ---------------------------

playlists_dict = {'2021': {'playlists':[], 'totalViewYear':0, 'countRaces': 0, 'viewsList':[]}, '2022':{'playlists':[], 'totalViewYear':0,'countRaces': 0, 'viewsList':[]}, '2023':{'playlists':[], 'totalViewYear':0, 'countRaces': 0, 'viewsList':[]}}

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
            if "Race Highlights" not in videos_info[index]['snippet']['title']:
                if "Qualifying Highlights" not in videos_info[index]['snippet']['title']:
                    index += 1
                else:
                    break
            else:
                break
        
        print(playlist['title'], videos_info[index]['snippet']['title'])
        video_id = videos_info[index]['snippet']['resourceId']['videoId']
        res = youtube.videos().list(part='statistics', id=video_id).execute()
        playlist['totalViews'] += int(res['items'][0]['statistics']['viewCount'])

        playlists_dict[year]['viewsList'].append(playlist['totalViews'])       
        playlists_dict[year]['totalViewYear'] += playlist['totalViews']      

# -------------- Terceira Etapa --------------------------- 

results = {'years': [], 'medians': [], 'averages': [], 'most_watched_race': [], 'totalViewRace':[], 'totalViewPerYear': []}

for year in playlists_dict:
    most_watched_race = max(playlists_dict[year]['playlists'], key=lambda x:x['totalViews'])
    results['years'].append(year)
    results['medians'].append(f"{median(playlists_dict[year]['viewsList']):.2f}")
    results['averages'].append(f"{mean(playlists_dict[year]['viewsList']):.2f}")
    title = most_watched_race['title'].replace("Formula 1", "")
    results['most_watched_race'].append(title)
    results['totalViewRace'].append(most_watched_race['totalViews'])
    results['totalViewPerYear'].append(playlists_dict[year]['totalViewYear'])

df = pd.DataFrame(results)
print(df)

# -------------- Quarta Etapa --------------------------- 

