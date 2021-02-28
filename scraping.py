import time
from datetime import date

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Links de cada site
kabum = {'HD': 'https://www.kabum.com.br/hardware/disco-rigido-hd/sata-3-5',
         'Fonte': 'https://www.kabum.com.br/hardware/fontes?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
         'RAM': 'https://www.kabum.com.br/hardware/memoria-ram?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
         'GPU': 'https://www.kabum.com.br/hardware/placa-de-video-vga?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
         'Placamae': 'https://www.kabum.com.br/hardware/placas-mae?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
         'Processador': 'https://www.kabum.com.br/hardware/processadores?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
         'SSD': 'https://www.kabum.com.br/hardware/ssd-2-5?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]'
         }

tbshop = {'HD': '',
          'Fonte': '',
          'RAM': '',
          'GPU': '',
          'Placamae': '',
          'Processador': '',
          'SSD': ''}

pichau = {'HD': '',
          'Fonte': '',
          'RAM': '',
          'GPU': '',
          'Placamae': '',
          'Processador': '',
          'SSD': ''}

# Pegar todas as descricoes e salvar em csvs
lista_sites = [kabum, tbshop, pichau]

# Making Selenium driver headless and supressing some messages
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=chrome_options)

for website in lista_sites:
    if website == kabum:
        site = 'Kabum'
    elif website == tbshop:
        site = 'Terabyte Shop'
        break
    else:
        site = 'Pichau'
        break

    print(f'Scraping {site}...')
    for categoria, link in website.items():
        print(f'    {categoria}')
        total_execution_time = 0
        produtos = {'site': [], 'descricao': [], 'marca': [], 'cartao': [], 'boleto': [], 'data': []}

        driver.get(link)
        time.sleep(2)
        pagina = 1

        while True:
            start_time_page = time.time()
            botao = driver.find_elements_by_xpath("//div[@class='sc-fznWOq hEjrXm']")

            lista_produtos = driver.find_elements_by_xpath("//div[@class='sc-fzqARJ eITELq']")

            for produto in lista_produtos:
                descricao = produto.find_element_by_xpath(".//a[@class='sc-fzoLsD gnrNhT item-nome']").text
                marca = produto.find_element_by_xpath(".//img[@class='sc-fznyAO brXUpP']").get_attribute('alt')
                cartao = produto.find_element_by_xpath(".//div[@class='sc-fznxsB ksiZrQ']").text
                boleto = produto.find_element_by_xpath(".//div[@class='sc-fznWqX qatGF']").text
                data = date.today()

                produtos['site'].append(site)
                produtos['descricao'].append(descricao)
                produtos['marca'].append(marca)
                produtos['cartao'].append(cartao)
                produtos['boleto'].append(boleto)
                produtos['data'].append(data)
            execution_time = time.time() - start_time_page

            print(f'    Page {pagina} - Execution time: {execution_time:.1f}s')
            total_execution_time += execution_time

            if len(botao):
                driver.execute_script("arguments[0].click();", botao[0])
                # botao[0].click()
                time.sleep(2)
                pagina += 1
            else:
                break

        nome_csv = 'data/' + str(categoria) + '.csv'
        produtos = pd.DataFrame.from_dict(produtos)
        produtos.to_csv(nome_csv, encoding='utf-8', index=False)
        print(f'    Total execution time: {total_execution_time:.1f}s\n')
driver.quit()
