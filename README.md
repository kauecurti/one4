Segue a documentação de como executar o arquivo "extracao-diario-jt.py":

Certifique-se de ter o Python 3.x instalado no seu computador.
Abra o terminal ou prompt de comando.
Instale as bibliotecas necessárias executando os seguintes comandos:

pip install selenium
pip install webdriver_manager
pip install pandas
Baixe o arquivo "extracao-diario-jt.py".
Abra o arquivo em um editor de texto ou IDE.
Altere o caminho onde será salvo o arquivo "resultados.xlsx" na última linha do código.
Execute o código no terminal ou prompt de comando com o seguinte comando:

python extracao-diario-jt.py
O processo de extração pode demorar alguns minutos, dependendo da quantidade de dados que serão coletados.
Após a execução, o arquivo "resultados.xlsx" será salvo no caminho especificado.



Documentação do código em Python

O código em Python abaixo usa a biblioteca Selenium para acessar o site https://dejt.jt.jus.br/dejt/f/n/diariocon, preencher um formulário com datas e clicar em um botão para pesquisar. Em seguida, ele extrai informações de várias páginas de resultados e salva os dados em um arquivo Excel.

Importando as bibliotecas necessárias


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
import sqlite3
As bibliotecas necessárias são importadas. A biblioteca Selenium é usada para automatizar a interação com o site e a biblioteca Pandas é usada para salvar os dados em um arquivo Excel.

Configurando o webdriver do Chrome


servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")
navegador = webdriver.Chrome(service=servico)
O webdriver do Chrome é configurado com a ajuda da biblioteca webdriver_manager e definido como headless para executar o código sem abrir o navegador em si.

Acessando o site e preenchendo o formulário


navegador.get('https://dejt.jt.jus.br/dejt/f/n/diariocon')

seven_days_ago = datetime.date.fromordinal(datetime.date.today().toordinal()-7).strftime("%d%m%Y")

date_now = datetime.date.fromordinal(datetime.date.today().toordinal()).strftime("%d%m%Y")
time.sleep(4)

navegador.find_element('xpath', '//*[@id="corpo:formulario:dataIni"]'
                        ).clear()

teste = navegador.find_element_by_xpath('//*[@id="corpo:formulario:dataIni"]')

time.sleep(3)
teste.send_keys(seven_days_ago)
navegador.find_element('xpath', '//*[@id="corpo:formulario:dataFim"]'
                        ).clear()

teste2 = navegador.find_element_by_xpath('//*[@id="corpo:formulario:dataFim"]')
time.sleep(3)
teste2.send_keys(date_now)

navegador.find_element('xpath', '//*[@id="corpo:formulario:botaoAcaoPesquisar"]'
                        ).click()
O site é acessado e as datas são preenchidas no formulário usando a biblioteca datetime. Em seguida, o botão de pesquisa é clicado.

Extrair dados da página atual e verificar se há uma próxima página


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
    data_de_disponibilizacao = navegador
