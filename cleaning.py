import os
import re
from datetime import date

import numpy as np
import pandas as pd
import sqlalchemy
import uuid

import utils
import variables


engine = sqlalchemy.create_engine(
    f"{variables.RDBMS}://{variables.USERNAME}:{variables.PASSWORD}@{variables.HOST}/{variables.DATABASE}"
)

con = engine.connect()


for csv in categorias:
    print(f'Starting: {csv}')
    if csv == 'placamae.csv':
        indice_site = 0
    else:
        indice_site = 1

    nome_categoria = csv.split('.')[0]
    csv_path = 'data/' + csv

    # Inicializando dataframes
    df_produto = pd.DataFrame(columns=colunas[nome_categoria])
    df_valores = pd.DataFrame(columns=['code', 'cartao', 'boleto', 'data'])

    # DataFrame do CSV e do banco
    df_scraping = pd.read_csv(csv_path)
    df_banco = pd.read_sql_table(nome_categoria, con)

    # Codigos e IDs do banco
    df_banco_codes = df_banco[['id', 'code']]
    df_banco = df_banco.drop(columns=['id', 'code'])

    # Realizando limpeza do DataFrame do CSV
    df_scraping_produto, df_scraping_valores = utils.df_clean(csv_path)

    # Loop em cada produto
    print(f'    Looping each product...')
    for indice, produto in enumerate(df_scraping_produto.values):
        indice_duplicado = df_banco[(df_banco == produto).all(axis=1)].index.values

        # SE FOR duplicado
        if len(indice_duplicado) > 0:
            indice_duplicado = int(indice_duplicado)
            code_duplicado = df_banco_codes['code'].loc[indice_duplicado]  # Pegando o Codigo do duplicado
            print(f'    Duplicate Code: {code_duplicado}')

            # Dicionario para adicionar o codigo
            valor_dict = {'code': code_duplicado,
                          'cartao': df_scraping_valores['cartao'].loc[indice],
                          'boleto': df_scraping_valores['boleto'].loc[indice],
                          'data': df_scraping_valores['data'].loc[indice]}
            df_valores = df_valores.append(valor_dict, ignore_index=True)

        # SE NAO for duplicado
        else:
            codigos_site = df_banco_codes['code'].loc[df_banco_codes['code'].str.findall('^' + siglas[produto[indice_site]]).index.values]
            if len(codigos_site) == 0:
                indice_novo = 0
            else:
                indice_novo = max(codigos_site.str.split('-', expand=True)[2].astype(int)) + 1

            codigo_novo = siglas[produto[indice_site]] + '-' + siglas[nome_categoria] + '-' + str(indice_novo)
            print(f'    New Code: {codigo_novo}')
            valor_dict = {'code': codigo_novo,
                          'cartao': df_scraping_valores['cartao'].loc[indice],
                          'boleto': df_scraping_valores['boleto'].loc[indice],
                          'data': df_scraping_valores['data'].loc[indice]}
            produto = np.insert(produto, 0, codigo_novo)
            produto = np.insert(produto, 0, indice_novo)
            produto = pd.Series(produto, index=colunas[nome_categoria])

            df_valores = df_valores.append(valor_dict, ignore_index=True)
            df_produto = df_produto.append(produto, ignore_index=True)

            df_banco_codes = df_banco_codes.append(produto[['id', 'code']], ignore_index=True)

    print(f'Finished: {csv}')
    print('\n-------------\n')
    df_valores.to_sql(name='valores', con=con, if_exists='append', index=False)
    df_produto.to_sql(name=nome_categoria, con=con, if_exists='append', index=False)
