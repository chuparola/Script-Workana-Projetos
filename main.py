import time
from bs4 import BeautifulSoup
import requests

class ExtratorProjetosWorkana:
    def __init__(self, link: str):
        self.link = link
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/154.0.0.0 Safari/537.36 Edg/154.0.0.0'
            ),
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.TOKEN = '8792434876:AAEe7rbFWH_-2XfSAenZzHrtwkHlXV1A0I8'
        self.CHAT_ID = '8061858940'

    def envia_projeto_telegram(self, texto: str):
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendMessage'

        dados = {
            'chat_id': self.CHAT_ID,
            'text': texto
        }

        requests.post(url, data=dados)

    def faz_ligacao(self):
        resposta = requests.get(self.link, headers=self.headers, timeout=15)

        if resposta.status_code != 200:
            print('Requição negada!')
            return    

        return resposta

    def extrai_projetos(self):
        titulo_projeto_antigo = ''
        
        while True:
            resposta = self.faz_ligacao()
            dados = resposta.json()

            titulo_projeto_atual = BeautifulSoup(dados['results']['results'][0]['title'], 'html.parser').find('span')['title']
            descricao_projeto = dados['results']['results'][0]['description']
            data_projeto = dados['results']['results'][0]['postedDate']
            valor_projeto = dados['results']['results'][0]['budget']
            link_projeto = 'https://www.workana.com' + BeautifulSoup(dados['results']['results'][0]['title'], 'html.parser').find('a')['href']

            print(titulo_projeto_antigo, titulo_projeto_atual, '\n')

            if titulo_projeto_antigo != titulo_projeto_atual:
                titulo_projeto_antigo = titulo_projeto_atual

                texto = f'{titulo_projeto_atual}\n\n{descricao_projeto}\n\n{data_projeto}\n\n{valor_projeto}\n\n{link_projeto}'

                self.envia_projeto_telegram(texto)

            time.sleep(1)

extrator = ExtratorProjetosWorkana('https://www.workana.com/pt/jobs?language=pt&skills=python')
extrator.extrai_projetos()
