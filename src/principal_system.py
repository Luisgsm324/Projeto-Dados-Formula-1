from data_system import Data_system
import os
import time

class Principal_system:
    def small_load(self):
        time.sleep(1)
        os.system('cls')

    def main(self):
        print(f"---------- Bem vindo ----------\nForneça as seguintes informações:")
        api_key = input("Insira a chave API do Youtube: ")
        question = input("Você deseja seguir a configuração padrão?\n Configuração padrão: Dados extraídos do canal da Fórmula 1 dos anos de 2021, 2022 e 2023 correspondentes às corridas realizadas\n[Y/N]: ")
        if question.upper() == "Y":
            print("Seguindo configuração padrão!")
            channel_id = "UCB_qr75-ydFVKSF9Dmo6izg"
            keywords_list = ["Grand Prix", "Gran Premio", "Grosser Preis", "Grossen Preis", "Grande Premio", "Grande Prêmio", "Magyar Nagydij"]
            years_selected = ["2021", "2022", "2023"]
        else:
            channel_id = input("Insira o ID do canal do Youtube: ")
            keyword = ""
            keywords_list = []
            while keyword != "Q":
                keyword = input("Insira as palavras chaves para pesquisa das playlists (Digite Q para terminar): ")
                if keyword != "Q":
                    keywords_list.append(keyword)
            years_selected = input("Insira os anos das playlists pretendidas: ").split()
            years_selected.sort()
        
        self.small_load()
        data_system = Data_system(api_key, channel_id, keywords_list, years_selected)
        print("Configuração finalizada. Processamento das informações sendo realizada...")
        data_system.load_informations()
        self.small_load()
        print("Processamento finalizado!") 
        self.small_load()
        methods_choice = {"1": data_system.acess_info_geral, "2": data_system.acess_info_year, "3": data_system.acess_info_runs, "4": None}
        while True:
            print("Quais ações você deseja realizar?\n[1] Mostrar panorama geral em tabela\n[2] Mostrar métricas de cada ano\n[3] Mostrar corridas dos anos em ordem\n[4] Sair")
            question = input()
            if question in methods_choice.keys():
                if question != "4":
                    self.small_load()
                    methods_choice[question]()
                    question = input("Clique enter para sair.")
                    self.small_load()
                else:
                    print("Finalizando sessão.")
                    break
            else:
                print("Opção inválida. Tente novamente!")
                self.small_load

sistema = Principal_system()
sistema.main()


