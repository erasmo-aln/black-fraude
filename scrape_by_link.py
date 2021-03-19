from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
from datetime import date

options = Options()
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)

link = input('Insert link: ')

driver.get(link)

csv = pd.DataFrame(columns=['descricao', 'boleto', 'cartao'])

boleto = driver.find_element_by_xpath(".//span[@class='preco_desconto_avista-cm']").text
cartao = driver.find_element_by_xpath(".//div[@class='preco_desconto-cm']").text
descricao = driver.find_element_by_xpath(".//h1[@class='titulo_det']").text
data = str(date.today())

csv = csv.append({'descricao': descricao, 'boleto': boleto, 'cartao': cartao, 'data': data}, ignore_index=True)

if 'produto.csv' in os.listdir():
    csv.to_csv('produto.csv', mode='a', header=False, index=False)
else:
    csv.to_csv('produto.csv', index=False)
