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

playlists_dict = {'2021': [], '2022':[], '2023':[]}

count = 0
break_condition = False

while True:
    res = youtube.playlists().list(part='snippet', channelId=formula1_channelID, pageToken=next_page_token).execute()
    # Para conseguir achar o título você chega nessa parte v 
    title = res['items'][0]['snippet']['title']
    for element in res['items']:
        playlist_data = element['snippet']
        title = playlist_data['title']
        year_publi = element['snippet']['publishedAt'].split("-")[0]
        if int(year_publi) >= 2021:
            for word in grand_prix_words:
                for year in searched_years:
                    if word in title and year == year_publi:
                        #print(title)
                        id = element['id']
                        playlists_dict[year_publi].append(id)
                        count += 1
        # Quando o ano for menor que 2021, não tem mais necessidade de continuar a procurar em todas as playlist, então tornamos uma variável True para que se dê um break no loop
        else:
            break_condition = True
    
    if break_condition:
        break
    playlist_id = res['items'][0]['id']
    next_page_token = res.get('nextPageToken')

for ids_list in playlists_dict.values():
    for id in ids_list:
        print(id)        
#print(playlists_dict)
print(count)