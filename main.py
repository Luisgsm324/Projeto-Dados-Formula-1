"""
{09/03/2024} -> 
Primeiro teste para conseguir os ID's da playlist.
"""
from googleapiclient.discovery import build

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
4º Etapa: Determinar a corrida mais vista entre os anos;
=============================

"""

# -------------- Primeira Etapa ---------------------------

playlists_dict = {'2021': {'playlists':[], 'totalCountYear':0}, '2022':{'playlists':[], 'totalCountYear':0}, '2023':{'playlists':[], 'totalCountYear':0}}

count = 0
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
                        count += 1
        # Quando o ano for menor que 2021, não tem mais necessidade de continuar a procurar em todas as playlist, então tornamos uma variável True para que se dê um break no loop
        else:
            break_condition = True
    
    if break_condition:
        break
    
    next_page_token = res.get('nextPageToken')

# -------------- Segunda Etapa ---------------------------
 
for year in playlists_dict.keys():
    print(year)
    for playlist in playlists_dict[year]['playlists']:
        #print(playlist['title'])
        res = youtube.playlistItems().list(part='snippet', maxResults=100, playlistId=playlist['id']).execute()
        videos_info = res['items']
        for video in videos_info:
            video_id = video['snippet']['resourceId']['videoId']
            res = youtube.videos().list(part='statistics', id=video_id).execute()
            
            # Essa condição foi criada para as situações em que existem playlists que tem certos problemas, como vídeos que estão indisponíveis ou ocultos.
            if len(res['items']) != 0:
                playlist['totalViews'] += int(res['items'][0]['statistics']['viewCount'])
                 
        playlists_dict[year]['totalCountYear'] += playlist['totalViews']      

# -------------- Terceira Etapa --------------------------- 

most_watched_race_2021 = max(playlists_dict['2021']['playlists'], key=lambda x:x['totalViews'])
print(f"A corrida mais assistida de 2021 foi: {most_watched_race_2021}")

most_watched_race_2022 = max(playlists_dict['2022']['playlists'], key=lambda x:x['totalViews'])
print(f"A corrida mais assistida de 2022 foi: {most_watched_race_2022}")

most_watched_race_2023 = max(playlists_dict['2023']['playlists'], key=lambda x:x['totalViews'])
print(f"A corrida mais assistida de 2023 foi: {most_watched_race_2023}")

# -------------- Quarta Etapa --------------------------- 


print(count)