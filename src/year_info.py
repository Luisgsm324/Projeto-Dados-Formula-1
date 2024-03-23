playlists_dict = {'2021': {'playlists':[], 'totalViewYear':0, 'countRaces': 0, 'viewsList':[]}, '2022':{'playlists':[], 'totalViewYear':0,'countRaces': 0, 'viewsList':[]}, '2023':{'playlists':[], 'totalViewYear':0, 'countRaces': 0, 'viewsList':[]}}

class Year_info:
    def __init__(self, year):
        self.year = year
        self.playlists_ids = []
        self.totalviewyear = 0
        self.countraces = 0
        self.viewslist = [] # Essa lista será utilizada para o cálculo da mediana