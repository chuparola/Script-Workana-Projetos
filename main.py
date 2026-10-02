import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class ExtratorProjetosWorkana:
    def __init__(self, link: str):
        self.link = link
        self.projetos_enviados = set()

        self.TOKEN = '8792434876:AAEe7rbFWH_-2XfSAenZzHrtwkHlXV1A0I8'
        self.CHAT_ID = '8061858940'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36')
        
        self.navegador = webdriver.Chrome(options=self.options)
        
    def envia_projeto_telegram(self, texto: str):
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendMessage'

        dados = {
            'chat_id': self.CHAT_ID,
            'text': texto
        }

        r = requests.post(url, data=dados)

        if r.status_code == 200:
            print('Projeto enviado pro bot no Telegram!')
            return

        print('Não foi possivel enviar o projeto para o Telegram.')

    def entra_url(self):
        self.navegador.get(self.link)

    def extrai_projetos(self):
        self.entra_url()

        titulo_projeto_antigo = ''
        
        while True:
            titulo_projeto_atual = WebDriverWait(self.navegador, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="project-item js-project"]/div/h2'))
            ).text

            descricao_projeto = WebDriverWait(self.navegador, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="project-item js-project"]/div[2]/div[2]'))
            ).text

            data_projeto = WebDriverWait(self.navegador, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="project-item js-project"]/div[1]'))
            ).text

            valor_projeto = WebDriverWait(self.navegador, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="project-item js-project"]/div[4]/p/span'))
            ).text

            link_projeto = WebDriverWait(self.navegador, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="project-item js-project"]/div/h2/span/a'))
            ).get_attribute('href')

            print(titulo_projeto_atual)

            if titulo_projeto_atual not in self.projetos_enviados:
                self.projetos_enviados.add(titulo_projeto_atual)
                texto = f'{titulo_projeto_atual}\n\n{descricao_projeto}\n\n{data_projeto}\n\n{valor_projeto}\n\n{link_projeto}'

                self.envia_projeto_telegram(texto)

            time.sleep(620)
            self.navegador.refresh()

extrator = ExtratorProjetosWorkana('https://www.workana.com/pt/jobs?language=pt&skills=python')
extrator.extrai_projetos()
