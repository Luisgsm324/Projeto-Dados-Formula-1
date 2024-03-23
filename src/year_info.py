class Year_info:
    def __init__(self, year):
        self.year = year
        self.playlists = []
        self.totalviewyear = 0
        self.countraces = 0
        self.viewslist = [] # Essa lista será utilizada para o cálculo da mediana

    def find_most_watched_race(self):
        most_watched_race = max(self.playlists, key=lambda x:x['totalViews'])
        return most_watched_race