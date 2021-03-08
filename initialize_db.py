import os
import re
from datetime import date

import numpy as np
import pandas as pd
import sqlalchemy
import uuid
from tqdm import tqdm

import utils
import variables














# teste = list(pd.read_csv('teste.csv')['id_product'])
# testando = pd.read_csv('testando.csv')
# valores = list(pd.read_csv('data/valores.csv')['code'])

# pbar = tqdm(total=len(testando))
# for index, linha in testando.iterrows():
#     codigo = linha['code']
#     uid = linha['id_product']

#     cont_codigo = valores.count(codigo)
#     cont_id = teste.count(uid)

#     if cont_codigo != cont_id:
#         print(codigo)
#         pbar.update(1)
#     else:
#         pbar.update(1)


#pd.set_option('display.expand_frame_repr', False)
# Create the engine and connect to the database
engine = sqlalchemy.create_engine(
    f"{variables.RDBMS}://{variables.USERNAME}:{variables.PASSWORD}@{variables.HOST}/{variables.DATABASE}"
)
con = engine.connect()

df = pd.read_csv('teste.csv')

# brands = pd.read_sql_table('brand', con)
# websites = pd.read_sql_table('website', con)

# valores = pd.read_csv('data/valores.csv')
# testando = pd.read_csv('testando.csv')

# product_db = pd.DataFrame(columns=['id', 'id_product', 'id_website', 'credit_card', 'cash', 'date'])

# pbar = tqdm(total=len(valores['code']))

# for index, linha in tqdm(valores.iterrows()):
#     if linha['code'] not in list(testando['code']):
#         pbar.update(1)
#         continue

#     new_id = uuid.uuid4()
#     id_product = testando['id_product'].loc[testando['code'] == linha['code']].values[0]
#     id_website = websites['id'].loc[websites['name'] == 'Kabum'].values[0]
#     cc = linha['cartao']
#     boleto = linha['boleto']
#     data = linha['data']

#     product_db = product_db.append({
#         'id': new_id,
#         'id_product': id_product,
#         'id_website': id_website,
#         'credit_card': cc,
#         'cash': boleto,
#         'date': data
#     }, ignore_index=True)
#     pbar.update(1)

# product_db.to_csv('teste.csv', index=False)




#     df_csv = pd.read_csv(path + csv)
#     df_csv = df_csv.drop_duplicates(subset=['descricao'])

#     for index, linha in df_csv.iterrows():
#         new_id = uuid.uuid4()
#         maincat_id = maincats['id'].loc[maincats['name'] == 'Hardware'].values[0]
#         subcat_id = subcats['id'].loc[subcats['name'] == cats[categoria]].values[0]
#         brand_id = brands['id'].loc[brands['name'] == linha['marca']].values[0]
#         description = linha['descricao']

#         product_db = product_db.append({'id': new_id, 'id_maincat': str(maincat_id),
#             'id_subcat': subcat_id, 'id_brand': brand_id, 'description': description}, ignore_index=True)

#         codes['code'].append(linha['code'])
#         codes['id_product'].append(new_id)

# pd.DataFrame.from_dict(codes).to_csv('testando.csv', index=False)
df.to_sql(name='pprice', con=con, if_exists='append', index=False)





        









#.to_sql(name='', con=con, if_exists='append', index=False)
    

    

        
    

    
    



