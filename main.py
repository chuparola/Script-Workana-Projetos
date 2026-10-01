from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--headless')
opcoes.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36')
navegador = webdriver.Chrome(options=opcoes)

navegador.get('https://www.workana.com/pt/jobs?language=pt&skills=python')

time.sleep(10)

try:
    projetos = WebDriverWait(navegador, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="project-item js-project"]'))
    )

    print(navegador.title, '\n')
    print(projetos.text)

except Exception as e:
    print('Provalvemente o CloudFlare apareceu!', e) 
