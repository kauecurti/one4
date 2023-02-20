from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import warnings
import csv
import time
import datetime

warnings.filterwarnings('ignore')

servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")
navegador = webdriver.Chrome(service=servico)

navegador.get('https://dejt.jt.jus.br/dejt/f/n/diariocon')

seven_days_ago = datetime.date.fromordinal(datetime.date.today().toordinal()-7).strftime("%d%m%Y")

date_now = datetime.date.fromordinal(datetime.date.today().toordinal()).strftime("%d%m%Y")
time.sleep(4)

navegador.find_element('xpath', '//*[@id="corpo:formulario:dataIni"]').clear()

teste = navegador.find_element_by_xpath('//*[@id="corpo:formulario:dataIni"]')

time.sleep(3)
teste.send_keys(seven_days_ago)
navegador.find_element('xpath', '//*[@id="corpo:formulario:dataFim"]'
                        ).clear()

teste2 = navegador.find_element_by_xpath('//*[@id="corpo:formulario:dataFim"]')
time.sleep(3)
teste2.send_keys(date_now)

navegador.find_element('xpath', '//*[@id="corpo:formulario:botaoAcaoPesquisar"]').click()

resultados = []

# Extrair os dados da página atual
data_de_disponibilizacao = navegador.find_elements_by_xpath('//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[1]')
titulo = navegador.find_elements_by_xpath('//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[2]/span')
for i in range(len(titulo)):
    resultados.append((data_de_disponibilizacao[i].text, titulo[i].text))

# Verificar se há uma próxima página
botao_proxima_pagina = navegador.find_elements_by_xpath('//*[@id="diarioInferiorNav"]/table/tbody/tr/td[1]/button[1]')

botao_proxima_pagina[0].click()

time.sleep(3)
while True:
    # Extrair os dados da página atual
    data_de_disponibilizacao = navegador.find_elements_by_xpath('//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[1]')
    titulo = navegador.find_elements_by_xpath('//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[2]/span')
    for i in range(len(titulo)):
        resultados.append((data_de_disponibilizacao[i].text, titulo[i].text))

    # Verificar se há uma próxima página
    botao_proxima_pagina2 = navegador.find_elements_by_xpath('//*[@id="diarioInferiorNav"]/table/tbody/tr/td[1]/button[3]')
    if botao_proxima_pagina2:
        for i in range(7):
            try:
                botao_proxima_pagina2[0].click()
               
                time.sleep(3) # Aguardar 3 segundos para carregar a próxima página
                data_de_disponibilizacao = navegador.find_elements_by_xpath('//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[1]')
                titulo = navegador.find_elements_by_xpath('//*[@id="diarioCon"]/fieldset/table/tbody/tr/td[2]/span')
                for j in range(len(titulo)):
                    resultados.append((data_de_disponibilizacao[j].text, titulo[j].text))
            except:
                
                break
    else:
        break



print(resultados)

df = pd.DataFrame(resultados)
df.to_excel('resultados.xlsx', index=False)

