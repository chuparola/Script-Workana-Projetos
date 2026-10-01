from selenium import webdriver

opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--headless')
opcoes.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36')
navegador = webdriver.Chrome(options=opcoes)

navegador.get('https://www.workana.com/pt/jobs?language=pt&skills=python')

print(navegador.page_source)
