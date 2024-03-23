from googleapiclient.discovery import build
from year_info import Year_info

class System(Year_info):
    def __init__(self, key, channel_id, selected_words, selected_dates):
        self.key = key
        self.channel_id = channel_id
        self.selected_words = selected_words
        self.selected_dates = []
        for date in selected_dates:
            self.selected_dates.append(Year_info(date))
        self.youtube = build('youtube', 'v3', developerKey=self.key)


    # Função para encontrar as playlists com os parâmetros informados
    def find_playlists(self):
        pass

sistema = System('AIzaSyCls8LWBEcyvriLk4PAS5io0NJWzZYj_9Q', 'UCB_qr75-ydFVKSF9Dmo6izg', ["Grand Prix", "Gran Premio", "Grosser Preis", "Grossen Preis", "Grande Premio", "Grande Prêmio", "Magyar Nagydij"], ["2023", "2022", "2021"])
