import pandas as pd
import re


def fonte_clean(csv_path):
    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    fonte = {'potencia': [],
             'sku': []}

    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Extraindo potencia
        potencia = re.search(r"[0-9]+[Ww]", descricao)
        potencia = potencia.group() if potencia is not None else 'NaN'

        # Extraindo SKU
        if df['marca'][indice] == 'Brazil PC':
            sku = re.search(r"[Bb][Pp][Cc].[0-9]+\w+", descricao).group()
        else:
            sku = descricao.split(' ')[-1].strip('()')

        # Adiciona produto limpo
        fonte['potencia'].append(potencia)
        fonte['sku'].append(sku)

    fonte = pd.DataFrame(fonte)

    # Limpando alguns SKU's inexistentes
    indexes = list(fonte.loc[(fonte['sku'] == 'Bronze') | (fonte['sku'] == 'Modular') | (fonte['sku'] == 'Semi-Modular') | (fonte['sku'] == '500W') | (fonte['sku'] == '600W') | (fonte['sku'] == '650W')].index)
    fonte['sku'][indexes] = 'NaN'

    # Adicionando SKU e Potencia ao dataframe final, retirando a descricao
    df.insert(0, 'sku', fonte['sku'])
    df.insert(4, 'potencia', fonte['potencia'])

    # Separando em dois dataframes
    df_valores = df[['cartao', 'boleto', 'data']]
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])

    return df_produto, df_valores


def gpu_clean(csv_path):
    gpu = {'sku': [],
           'modelo': [],
           'memoria': [],
           'gddr': []}

    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    # Excluindo os que não são placas
    indices = list()
    for indice, descricao in enumerate(df['descricao']):
        resultado = re.search('^[P][Ll][Aa][Cc][Aa]', descricao)
        if resultado is None:
            indices.append(indice)
    df = df.drop(index=indices).reset_index(drop=True)

    # Limpando descrição
    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Excluir 'Placa de video'
        texto = re.search(r'^[Pp][Ll][Aa][Cc][Aa]\s[Dd][Ee]\s[Vv][IiíÍ][Dd][Ee][Oo]', descricao).group()
        descricao = descricao.replace(texto, '').strip()

        # Excluir 'AMD' e 'Nvidia'
        texto = re.search('([Aa][Mm][Dd])|'
                          '([Nn][Vv][Ii][Dd][Ii][Aa])', descricao)
        if texto is not None:
            descricao = descricao.replace(texto.group(), '').strip()

        # Excluir 'GeForce' e 'Radeon'
        texto = re.search('([Gg][Ee][Ff][Oo][Rr][Cc][Ee])|'
                          '([Rr][Aa][Dd][Ee][Oo][Nn])', descricao)
        if texto is not None:
            descricao = descricao.replace(texto.group(), '')

        # Excluir Marca
        marca = df['marca'][indice]
        texto = re.search(marca, descricao, re.IGNORECASE)
        if texto is not None:
            descricao = descricao.replace(texto.group(), '')

    # Extraindo Caracteristicas
        # Extraindo SKU
        sku = descricao.split(' - ', maxsplit=1)
        if len(sku) > 1:
            sku = sku[1]
        else:
            sku = 'NaN'
        descricao = re.sub(sku, '', descricao, count=1).strip()  # Limpando descricao

        # Extraindo Memoria
        memoria = re.search('[0-9]+[Gg][Bb]', descricao)
        memoria = memoria.group() if memoria is not None else 'NaN'
        descricao = descricao.replace(memoria, '').strip()  # Limpando descricao

        # Extraindo GDDR
        gddr = re.search('[Gg]?[Dd][Dd][Rr][0-9]', descricao)
        #   Unificando DDR's com GDDR's
        if gddr is not None:
            if gddr.group()[0].lower() == 'd':
                gddr = 'GDDR' + gddr.group()[-1]
            else:
                gddr = gddr.group()
        else:
            gddr = 'NaN'
        descricao = descricao.replace(gddr, '').strip()  # Limpando descricao

        # Removendo 'lixo' da descricao (resultando no modelo)
        descricao = descricao.replace(',', '')
        descricao = re.sub(r'\s+', ' ', descricao).strip()
        descricao = re.sub(r'[\s-]$', '', descricao).strip()
        descricao = re.sub(r'^-\s', '', descricao).strip()
        descricao = re.sub(r'^VGA', '', descricao).strip()

        # Adicionando caracteristicas ao dataframe
        gpu['sku'].append(sku)
        gpu['modelo'].append(descricao)
        gpu['memoria'].append(memoria)
        gpu['gddr'].append(gddr)

    gpu = pd.DataFrame(gpu)

    # Substituindo Descricao pelas caracteristicas
    df.insert(0, 'sku', gpu['sku'])
    df.insert(4, 'modelo', gpu['modelo'])
    df.insert(5, 'memoria', gpu['memoria'])
    df.insert(6, 'gddr', gpu['gddr'])

    # Separando em dois dataframes
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])
    df_valores = df[['cartao', 'boleto', 'data']]

    return df_produto, df_valores


def hd_clean(csv_path):
    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    hd = {'capacidade': [],
          'sku': []}

    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Extraindo capacidade
        capacidade = re.search(r"[0-9]+[Tt][Bb]", descricao).group()

        # Extraindo SKU
        sku = descricao.split(' ')[-1]

        # Adicionando ao dataframe
        hd['capacidade'].append(capacidade)
        hd['sku'].append(sku)

    hd = pd.DataFrame(hd)

    # Substituindo Descricao pelas caracteristicas
    df.insert(0, 'sku', hd['sku'])
    df.insert(4, 'capacidade', hd['capacidade'])

    # Separando em dois dataframes
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])
    df_valores = df[['cartao', 'boleto', 'data']]

    return df_produto, df_valores


def placamae_clean(csv_path):
    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    placamae = {'modelo': [],
                'tamanho': [],
                'entrada': [],
                'socket': []}

    tamanhos = {'mATX': r'[m]-?[Aa][Tt][Xx]|[Mm][Ii][Cc][Rr][Oo][\s-][Aa][Tt][Xx]',
                'EATX': r'[Ee]-?[Aa][Tt][Xx]',
                'Mini ITX': r'[Mm][Ii][Nn][Ii][-\s][Ii][Tt][Xx]'}

    # Extraindo caracteristicas
    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Excluir 'Placa-Mãe'
        descricao = descricao.replace(descricao.split(' ')[0], '').strip()

        # Checar Marca
        if descricao.split(' ')[0] == df['marca'][indice]:
            descricao = descricao.replace(descricao.split(' ')[0], '').strip()
        else:
            descricao = descricao.replace(descricao.split(' ')[0], '').strip()
            if descricao.split(' ')[0] == df['marca'][indice]:
                descricao = descricao.replace(descricao.split(' ')[0], '', 1).strip()

        # Pegando Socket
        socket = re.search(r'([Aa][Mm][Dd]\s?)?[AaFf][Mm][0-9][.]?\b|'
                           r'(([Ii][Nn][Tt][Ee][Ll]\s?)?[Ll][Gg][Aa].?.?[0-9]+)|'
                           r'([Aa][Mm][Dd]\s?)?[Ss]?[Tt][Rr][Xx]?[40]+\b|'
                           r'([Ii][Nn][Tt][Ee][Ll]\s[0-9]+)|'
                           r'([Aa][Mm][Dd]\s?)?[Ss]?[Tt][Rr][Xx]?[0-9]|'
                           r'([Aa][Mm][Dd]\s)?[Ss]?[Tt][Rr][Xx][4]', descricao)
        socket = socket.group() if socket is not None else 'NaN'
        descricao = descricao.replace(socket, '')
        #   Excluindo Marca do socket
        marca_socket = socket.split(' ')[0]
        if marca_socket == 'Intel' or marca_socket == 'AMD':
            socket = socket.replace(marca_socket, '').strip()
        #   Unificando LGA's
        versao = re.search('[0-9][0-9][0-9][0-9]', socket)
        if versao is not None:
            socket = 'LGA ' + versao.group()

        # Pegando Tamanho
        # mATX, Micro ATX, eATX, E-ATX, mini-ITX, ATX
        tamanho = re.search(r'([MmEe])?.?[Aa][Tt][Xx]|'
                            r'([Xx][Ll]-?[Aa][Tt][Xx])|'
                            r'[Mm][Ii][NnCc][IiRr][Oo]?[\s-][AI][T][X]', descricao)
        tamanho = tamanho.group() if tamanho is not None else 'NaN'
        descricao = descricao.replace(tamanho, '')
        #   Unificando Tamanhos
        for key, value in tamanhos.items():
            tamanho_final = re.search(value, tamanho)
            if tamanho_final is not None:
                tamanho = key
                break

        # Pegando Entrada
        entrada = re.search(r'[Dd][Dd][Rr][34]', descricao)
        entrada = entrada.group() if entrada is not None else 'NaN'
        descricao = descricao.replace(entrada, '')

        # Excluindo info da descricao (Extraindo Modelo)
        descricao = descricao.replace(',', '').strip()
        descricao = re.sub(r'\s+', ' ', descricao).strip()
        descricao = re.sub(r'[p][/]\s?', '', descricao).strip()
        descricao = re.sub(r'^.\s', '', descricao).strip()

        # Adicionando ao dataframe
        placamae['modelo'].append(descricao)
        placamae['socket'].append(socket)
        placamae['tamanho'].append(tamanho)
        placamae['entrada'].append(entrada)

    placamae = pd.DataFrame(placamae)

    # Adicionando info no dataframe e excluindo descricao
    df.insert(3, 'modelo', placamae['modelo'])
    df.insert(4, 'tamanho', placamae['tamanho'])
    df.insert(5, 'entrada', placamae['entrada'])
    df.insert(6, 'socket', placamae['socket'])

    # Separando em dois dataframes
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])
    df_valores = df[['cartao', 'boleto', 'data']]

    return df_produto, df_valores


def processador_clean(csv_path):
    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    processador = {'sku': [],
                   'modelo': [],
                   'cache': [],
                   'frequencia': [],
                   'socket': []}

    # Excluindo itens que nao sao processadores
    indices = list()
    for indice, descricao in enumerate(df['descricao']):
        resultado = re.search('^Processador', descricao, re.IGNORECASE)
        if resultado is None:
            indices.append(indice)
    df = df.drop(index=indices).reset_index(drop=True)

    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Excluindo 'Processador'
        texto = re.search('Processador', descricao, re.IGNORECASE).group()
        descricao = descricao.replace(texto, '').strip()

        # Extraindo SKU
        sku = descricao.split(' - ')
        if len(sku) > 1:
            sku = sku[1].strip('-')
        else:
            sku = sku[0].split(' ')[-1].strip('-')
        descricao = descricao.replace(sku, '').strip()

        # Extraindo Socket
        socket = re.search(r'([Aa][Mm][Dd]\s?)?[AaFf][Mm][0-9][.]?\b|'
                           r'(([Ii][Nn][Tt][Ee][Ll]\s?)?[Ll][Gg][Aa].?.?[0-9]+)|'
                           r'([Aa][Mm][Dd]\s?)?[Ss]?[Tt][Rr][Xx]?[40]+\b|'
                           r'([Ii][Nn][Tt][Ee][Ll]\s[0-9]+)|'
                           r'([Aa][Mm][Dd]\s?)?[Ss]?[Tt][Rr][Xx]?[0-9]|'
                           r'([Aa][Mm][Dd]\s)?[Ss]?[Tt][Rr][Xx][4]', descricao)
        socket = socket.group() if socket is not None else 'NaN'
        descricao = descricao.replace(socket, '').strip()

        # Extraindo Frequencia
        frequencia = re.search(r'[0-9][0-9\.,]?[0-9]?[0-9]?\s?[GgMm][Hh][Zz]\s?(\((.*)\))?', descricao)
        frequencia = frequencia.group() if frequencia is not None else 'NaN'
        descricao = descricao.replace(frequencia, '').strip()

        # Extraindo cache
        cache = re.search(r'([Cc][Aa][Cc][Hh][Ee]\s?)?[0-9/.,]+[Mm][Bb]', descricao)
        cache = cache.group() if cache is not None else 'NaN'
        descricao = descricao.replace(cache, '').strip()
        cache = cache.replace('Cache', '').strip()

        # Limpando modelo
        modelo = re.split(r'\s\s+|,|\sc/\s', descricao)[0]
        modelo = re.sub(r'([Aa][Mm][Dd])|([Ii][Nn][Tt][Ee][Ll])', '', modelo).strip()

        # Adicionando ao dataframe
        processador['sku'].append(sku)
        processador['modelo'].append(modelo)
        processador['cache'].append(cache)
        processador['frequencia'].append(frequencia)
        processador['socket'].append(socket)

    processador = pd.DataFrame(processador)

    # Adicionando info no dataframe e excluindo descricao
    df.insert(0, 'sku', processador['sku'])
    df.insert(4, 'modelo', processador['modelo'])
    df.insert(5, 'cache', processador['cache'])
    df.insert(6, 'frequencia', processador['frequencia'])
    df.insert(7, 'socket', processador['socket'])

    # Separando em dois dataframes
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])
    df_valores = df[['cartao', 'boleto', 'data']]

    return df_produto, df_valores


def ram_clean(csv_path):
    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    ram = {'sku': [],
           'entrada': [],
           'frequencia': [],
           'capacidade': []}

    # Excluindo itens que nao sao memorias
    indices = list()
    for indice, descricao in enumerate(df['descricao']):
        resultado = re.search('^Memória', descricao, re.IGNORECASE)
        if resultado is None:
            indices.append(indice)
    df = df.drop(index=indices).reset_index(drop=True)

    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Extraindo SKU
        sku = descricao.split(' ')[-1]

        # Extraindo Marca
        marca = descricao.split(' ')[1].strip(',')
        if marca == 'G.SKill':
            marca = marca.replace('G.SKill', 'G.Skill')

        # Extraindo Entrada
        entrada = re.search(r'[A-Za-z][A-Za-z][A-Za-z][0-9]', descricao)
        entrada = entrada.group() if entrada is not None else 'NaN'

        # Extraindo Frequencia
        frequencia = re.search(r'([0-9]+[MmHhZz]+)|(M\.2)+', descricao)
        frequencia = frequencia.group() if frequencia is not None else 'NaN'

        # Extraindo Capacidade
        capacidade = re.search(r'[0-9]+\s*[Gg][Bb]', descricao)
        capacidade = capacidade.group() if capacidade is not None else 'NaN'
        #   Quantidade
        quantidade = re.search(r'\([0-9][Xx][0-9]+[Gg][Bb]\)', descricao)
        quantidade = quantidade.group() if quantidade is not None else ''

        # Adicionando ao dataframe
        ram['sku'].append(sku)
        ram['entrada'].append(entrada)
        ram['frequencia'].append(frequencia)
        ram['capacidade'].append(capacidade + ' ' + quantidade)

    ram = pd.DataFrame(ram)

    # Substituindo Descricao pelas caracteristicas
    df.insert(0, 'sku', ram['sku'])
    df.insert(4, 'entrada', ram['entrada'])
    df.insert(5, 'frequencia', ram['frequencia'])
    df.insert(6, 'capacidade', ram['capacidade'])

    # Separando em dois dataframes
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])
    df_valores = df[['cartao', 'boleto', 'data']]

    return df_produto, df_valores


def ssd_clean(csv_path):
    df = pd.read_csv(csv_path)

    # Removendo duplicados
    df.drop_duplicates(inplace=True, ignore_index=True)

    ssd = {'sku': [],
           'modelo': [],
           'capacidade': [],
           'entrada': [],
           'leitura': [],
           'escrita': []}

    # Removendo itens que nao sao SSD
    df = df.drop(index=list(df.loc[df['descricao'].str.split(' ', expand=True)[0] != 'SSD'].index)).reset_index(drop=True)
    df = df.drop(index=list(df.loc[df['descricao'].str.split(' ', expand=True)[1].isin(['Externo', 'Portátil'])].index)).reset_index(drop=True)
    df = df.drop(index=list(df.loc[df['descricao'].str.split(' ', expand=True)[2].isin(['Externo,', 'Portátil,'])].index)).reset_index(drop=True)

    # Removendo SSD da descricao
    df['descricao'] = df['descricao'].str.replace('SSD', '').str.strip()

    for indice, descricao in enumerate(df['descricao']):
        # Mudando valores para floats
        df['cartao'][indice] = float(df['cartao'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))
        df['boleto'][indice] = float(df['boleto'][indice].replace('R$ ', '').replace('.', '').replace(',', '.'))

        # Extraindo SKU
        sku = descricao.split(' - ')[-1]
        descricao = descricao.replace(sku, '').strip(' -')

        # Excluindo Marca
        if df['marca'][indice] == 'WD_Black':
            marca = 'WD Black'
        elif df['marca'][indice] == 'Western Digital':
            marca = 'WD'
        else:
            marca = df['marca'][indice]
        descricao = re.sub(fr'^.*?{marca}\s?', '', descricao, flags=re.I).strip(' ,')

        # Extraindo Capacidade
        capacidade = re.search(r'[0-9]+\s?[GgTt][Bb]', descricao).group()
        descricao = descricao.replace(capacidade, '')

        # Extraindo Leitura
        leitura = re.search(r'(leitura[s]?)?[:\s][\s]?[0-9][\.,]?[0-9]+\s?[M]?B/S', descricao, re.I)
        leitura = leitura.group() if leitura is not None else 'NaN'
        descricao = descricao.replace(leitura, '')
        #   Limpando Leitura
        leitura = re.search(r'[0-9]+\s?[M]?B/S', leitura, re.I)
        leitura = leitura.group() if leitura is not None else 'NaN'

        # Extraindo Escrita
        escrita = re.search(r'((gravaç[ãõ][oe][s]?)|(escrita[s]?))[:\s][\s]?[0-9][\.,]?[0-9]+\s?[M]?B/S', descricao, re.I)
        escrita = escrita.group() if escrita is not None else 'NaN'
        descricao = descricao.replace(escrita, '')
        #   Limpando Escrita
        escrita = re.search(r'[0-9]+\s?[M]?B/S', escrita, re.I)
        escrita = escrita.group() if escrita is not None else 'NaN'

        # Excluindo 'PCIe' e 'NVMe'
        descricao = re.sub('pcie', '', descricao, flags=re.I)
        descricao = re.sub('nvme', '', descricao, flags=re.I)

        # Extraindo Entrada
        entrada = re.search(r'(([m]?sata[\s]?)([3]|[i]+|2\.5.)?)|(M[\.]?2)', descricao, re.I)
        entrada = entrada.group() if entrada is not None else 'NaN'
        descricao = descricao.replace(entrada, '')
        entrada = entrada.replace(r'^SATA.*', 'SATA')
        entrada = entrada.replace(r'(M\.2)|M2', 'M.2')

        # Extraindo modelo
        modelo = descricao.split(',')[0].strip()
        if len(modelo) < 2:
            modelo = df['marca'][indice]

        # Adicionando ao dataframe
        ssd['sku'].append(sku)
        ssd['modelo'].append(modelo)
        ssd['capacidade'].append(capacidade)
        ssd['entrada'].append(entrada)
        ssd['leitura'].append(leitura)
        ssd['escrita'].append(escrita)

    ssd = pd.DataFrame(ssd)

    # Substituindo Descricao pelas caracteristicas
    df.insert(0, 'sku', ssd['sku'])
    df.insert(4, 'modelo', ssd['modelo'])
    df.insert(5, 'capacidade', ssd['capacidade'])
    df.insert(6, 'entrada', ssd['entrada'])
    df.insert(7, 'leitura', ssd['leitura'])
    df.insert(8, 'escrita', ssd['escrita'])

    # Separando em dois dataframes
    df_produto = df.drop(columns=['cartao', 'boleto', 'data'])
    df_valores = df[['cartao', 'boleto', 'data']]

    return df_produto, df_valores


def df_clean(csv_path):
    categoria = csv_path.split('/')[1].split('.')[0]

    funcoes = {'fonte': fonte_clean,
               'gpu': gpu_clean,
               'hd': hd_clean,
               'placamae': placamae_clean,
               'processador': processador_clean,
               'ram': ram_clean,
               'ssd': ssd_clean}

    if categoria in funcoes:
        df_produto, df_valores = funcoes[categoria](csv_path)

    return df_produto, df_valores
