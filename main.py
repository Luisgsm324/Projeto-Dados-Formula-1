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
2º Etapa: Fazer um somatório da corrida com mais visualização em cada ano; 
3º Etapa: Determinar o ano com mais visualização;
4º Etapa: Determinar a corrida mais vista entre os anos;
=============================

"""

# -------------- Primeira Etapa ---------------------------

playlists_dict = {'2021': [], '2022':[], '2023':[]}

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
                        info_dict = {'id':None, 'title':None, 'id_videos': [], 'totalViews': 0 }
                        info_dict['id'], info_dict['title'] = element['id'], title
                        playlists_dict[year_publi].append(info_dict)
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
    for playlist in playlists_dict[year]:
        #print(playlist['title'])
        res = youtube.playlistItems().list(part='snippet', maxResults=100, playlistId=playlist['id']).execute()
        videos_info = res['items']
        #print(len(videos_info))
        for video in videos_info:
            video_id = video['id']
            #print(video_id)
            #res = youtube.videos().list(part='statistics', id=video_id).execute()
            #print(res)
            #playlist['totalViews'] += int(res['items'][0]['statistics']['viewCount'])
            #print(video['snippet']['title'])
            #print(video['snippet'].keys())
        print(playlist['title'],playlist['totalViews'])       
        print("-----")
            

print(count)