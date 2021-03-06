# Scraping-related variables
websites = {
    'Kabum': 0,
    'Pichau': 1
}

# Key = The main category
# Value = List (or an element) of sub categories
categories = {
    'Hardware': ['HD', 'PowerSupply', 'RAM', 'GPU', 'Motherboard', 'Processor', 'SSD'],
    'Peripherals': [],
    'Notebooks': []
}

# Key = All sub categories
# Value = URL associated with 'websites' dictionary's indexes.
links = {
    'HD': [
        'https://www.kabum.com.br/hardware/disco-rigido-hd/sata-3-5',
        'https://www.pichau.com.br/hardware/hard-disk-e-ssd?p=1&product_list_order=name&product_list_limit=48'
    ],
    'PowerSupply': [
        'https://www.kabum.com.br/hardware/fontes?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
        'https://www.pichau.com.br/hardware/fonte?p=1&product_list_limit=48&product_list_order=name'
    ],
    'RAM': [
        'https://www.kabum.com.br/hardware/memoria-ram?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
        'https://www.pichau.com.br/hardware/memorias?p=1&product_list_limit=48&product_list_order=name'
    ],
    'GPU': [
        'https://www.kabum.com.br/hardware/placa-de-video-vga?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
        'https://www.pichau.com.br/hardware/placa-de-video?p=1&product_list_limit=48&product_list_order=name'
    ],
    'Motherboard': [
        'https://www.kabum.com.br/hardware/placas-mae?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
        'https://www.pichau.com.br/hardware/placa-m-e?p=1&product_list_limit=48&product_list_order=name'
    ],
    'Processor': [
        'https://www.kabum.com.br/hardware/processadores?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
        'https://www.pichau.com.br/hardware/processadores?p=1&product_list_limit=48&product_list_order=name'
    ],
    'SSD': [
        'https://www.kabum.com.br/hardware/ssd-2-5?pagina=1&ordem=6&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]',
        'https://www.pichau.com.br/hardware/ssd?p=1&product_list_limit=48&product_list_order=name'
    ]
}

# Each key represents an element on the page. The values are XPaths associated with
# each element and 'websites' dict indexes.
xpaths = {
    'NextPage': [
        "//div[@class=\'sc-fznWOq hEjrXm\']",
        ''
    ],
    'Products': [
        "//div[@class=\'sc-fzqARJ eITELq\']",
        ''
    ],
    'Description': [
        ".//a[@class=\'sc-fzoLsD gnrNhT item-nome\']",
        ''
    ],
    'Brand': [
        ".//img[@class=\'sc-fznyAO brXUpP\']",
        ''
    ],
    'CreditCard': [
        ".//div[@class=\'sc-fznxsB ksiZrQ\']",
        ''
    ],
    'Cash': [
        ".//div[@class=\'sc-fznWqX qatGF\']"
    ]
}

# Options for the chromedriver
driver_options_list = [
    "start-maximized",
    "enable-automation",
    "window-size=1400,1500",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-infobars",
    "--disable-dev-shm-usage",
    "--log-level=3"
]

# DataFrame format for raw product's table (before cleaning phase)
product_dataframe = {
    'Website': [],
    'Description': [],
    'Brand': [],
    'CreditCard': [],
    'Cash': [],
    'Date': []
}