from googleapiclient.discovery import build
from year_info import Year_info
import pandas as pd
from tabulate import tabulate

class Data_system(Year_info):
    def __init__(self, key, channel_id, selected_words, selected_dates):
        self.key = key
        self.channel_id = channel_id
        self.selected_words = selected_words
        self.selected_dates = [] # Esse parâmetro vai armazenar as principais informações que serão acessadas
        for date in selected_dates:
            self.selected_dates.append(Year_info(date))
        self.youtube = build('youtube', 'v3', developerKey=self.key)
    
    def acess_info_runs(self):
        for year_info in self.selected_dates:
            results = []
            print(f"Corridas realizadas no ano de {year_info.year}")
            count = 0
            for playlist_info in year_info.playlists:
                ref = (playlist_info['title'], playlist_info['totalViews'])
                results.append(ref)
            results.sort(reverse=True, key=lambda x:x[1])
            for element in results:
                count += 1
                print(f"{count} - {element[0]} - {element[1]}")
            print(f"Foram realizadas {count} corridas na temporada de {year_info.year}\n-------------------")

    def acess_info_geral(self):
        # Dicionário que será disposto para mostrar os resultados
        results = {'years': [], 'medians': [], 'averages': [], 'most_watched_race': [], 'totalViewRace':[], 'totalViewPerYear': []}
        for year_info in self.selected_dates:
            most_watched_race = year_info.find_racetitle()
            median_year = year_info.find_median()
            average_year = year_info.find_average()
            totalviewsrace = year_info.find_totalviewsrace()
            totalviewsyear = year_info.find_totalviewsyear()

            results['years'].append(year_info.year)
            results['medians'].append(median_year)
            results['averages'].append(average_year)
            results['most_watched_race'].append(most_watched_race)
            results['totalViewRace'].append(totalviewsrace)
            results['totalViewPerYear'].append(totalviewsyear)
        
        df = pd.DataFrame(results)
        headers_list = ["Ano", "Mediana", "Média", "Corrida mais vista", "Views Corrida", "Views Ano Total"]
        print(tabulate(df, headers=headers_list, tablefmt='grid'))

    def acess_info_year(self):
        print("------- Panorama geral dos anos -------")
        for year_info in self.selected_dates:
            most_watched_race = year_info.find_most_watched_race()
            print(f"{year_info.year} registrou um total de {year_info.countraces} corridas ao decorrer do ano.\nO total de visualizações foi {year_info.totalviewyear} e a corrida mais assistida foi {most_watched_race['title']} com {most_watched_race['totalViews']}")   
    
    def load_informations(self): # Função para encontrar as playlists com os parâmetros informados
        print("Carregando...")
        # Variável criada com o intuito de parar de buscar mais playlists, melhorando a otimização
        break_condition = False
        next_page_token = None
        
        while True:
            res = self.youtube.playlists().list(part='snippet', channelId=self.channel_id, pageToken=next_page_token).execute()
            for element in res['items']:
                year_publi = element['snippet']['publishedAt'].split("-")[0]
                title = element['snippet']['title']
                if int(year_publi) >= int(self.selected_dates[0].year):
                    for word in self.selected_words:
                        for year_info_object in self.selected_dates:
                            if word in title and year_info_object.year == year_publi:
                                info_dict = {'id':None, 'title':None, 'totalViews': 0 }
                                info_dict['id'], info_dict['title'] = element['id'], title
                                year_info_object.playlists.append(info_dict)
                                year_info_object.countraces += 1
                # Quando o ano for menor que 2021, não tem mais necessidade de continuar a procurar em todas as playlist, então tornamos uma variável True para que se dê um break no loop
                else:
                    break_condition = True
            
            if break_condition:
                break
            
            next_page_token = res.get('nextPageToken')
        
        for year_info in self.selected_dates:
            for playlist in year_info.playlists:
                # Essa variável foi criado com o propósito de procurar o vídeo correspondentes aos highlights da corrida (Em certas situações ele não é o primeiro elemento)
                index = 0
                res = self.youtube.playlistItems().list(part='snippet', maxResults=100, playlistId=playlist['id']).execute()
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
                res = self.youtube.videos().list(part='statistics', id=video_id).execute()
                playlist['totalViews'] += int(res['items'][0]['statistics']['viewCount'])

                year_info.viewslist.append(playlist['totalViews'])       
                year_info.totalviewyear += playlist['totalViews']               

        print("Processo finalizado :)")
    