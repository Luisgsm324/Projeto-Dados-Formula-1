from statistics import median
from babel.numbers import format_compact_decimal, format_decimal

class Year_info:
    def __init__(self, year):
        self.year = year
        self.playlists = []
        self.totalviewyear = 0
        self.countraces = 0
        self.viewslist = [] # Essa lista será utilizada para o cálculo da mediana
        self.most_watched_race = None

    def find_most_watched_race(self):
        if self.most_watched_race is None:
            most_watched_race = max(self.playlists, key=lambda x:x['totalViews'])
            self.most_watched_race = most_watched_race
            return self.most_watched_race
        return self.most_watched_race

    def find_racetitle(self):
        if self.most_watched_race is not None:
            result = self.most_watched_race['title'].replace("Formula 1", "")
            return result
        result = self.find_most_watched_race()
        formated_result = self.most_watched_race['title'].replace("Formula 1", "")
        return formated_result
        

    def find_median(self):
        result = median(self.viewslist)
        formated_result = format_compact_decimal(result, format_type='short', fraction_digits=2, locale='pt_BR')
        return formated_result
    
    def find_average(self):
        result = sum(self.viewslist)/len(self.viewslist)
        formated_result = format_compact_decimal(result, format_type='short', fraction_digits=2, locale='pt_BR')
        return formated_result
            
    def find_totalviewsrace(self):
        result = format_decimal(self.most_watched_race['totalViews'])
        return result 

    def find_totalviewsyear(self):
        result = format_decimal(self.totalviewyear)
        return result 