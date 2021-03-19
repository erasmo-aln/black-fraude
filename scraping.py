import time
import uuid
import random
from datetime import date

import pandas as pd
import sqlalchemy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import variables
import scraper_utils


# Connect to the database
engine = sqlalchemy.create_engine(
    f"{variables.RDBMS}://{variables.USERNAME}:{variables.PASSWORD}@{variables.HOST}/{variables.DATABASE}"
)
connection = engine.connect()

print('Extracting database table\'s data')
# Get product table, to check if there are new ones
product_table = pd.read_sql_table(table_name='product', con=connection)[['id', 'description']]

# Get pprice table, filtering by today's date, to prevent duplicate entries
pprice_table = pd.read_sql_table(table_name='pprice', con=connection)[['id_product', 'date']]
# Convert the dataframe to a list with every id_product that already have been scraped
pprice_table = list(pprice_table.loc[pprice_table['date'] == str(date.today())]['id_product'])

# Get maincat (main category) table, to convert strings to uuid
maincat_values = list(variables.categories.keys())
maincat_table = pd.read_sql_table(table_name='maincat', con=connection)[['id', 'name']]

# Get subcat (sub-category) table, to convert strings to uuid
subcat_values = list(pd.core.common.flatten(list(variables.categories.values())))
subcat_table = pd.read_sql_table(table_name='subcat', con=connection)[['id', 'name']]

# Get brand table, to convert strings to uuid
brand_table = pd.read_sql_table(table_name='brand', con=connection)[['id', 'name']]

# Get brand table, to convert strings to uuid
website_table = pd.read_sql_table(table_name='website', con=connection)[['id', 'name']]

# Initialize chromedriver with predefined options
chrome_options = scraper_utils.set_driver_options()
driver = webdriver.Chrome(options=chrome_options)

print('Scraping started...')
for website_name, website_index in variables.websites.items():
    if website_name != 'Kabum':
        break
    for main_category, sub_category_list in variables.categories.items():
        if main_category != 'Hardware':
            break
        for sub_category in sub_category_list:

            # Reset these for each loop
            page = 1
            total_execution_time = 0
            link = variables.links[sub_category][website_index]
            product_dataframe = pd.DataFrame(variables.product_dataframe)

            print(f'\n{website_name} - {main_category} - {sub_category}:')

            driver.get(link)
            time.sleep(random.uniform(3, 8))  # Need to change

            # Looping through pages
            while True:
                page_start_time = time.time()

                # Get all page's products
                next_page_button = driver.find_elements_by_xpath(variables.xpaths['NextPage'][website_index])
                product_list = driver.find_elements_by_xpath(variables.xpaths['Products'][website_index])

                # Looping through products
                for product_element in product_list:

                    # Add the 'product_info' dictionary as a row in the dataframe
                    product_info = scraper_utils.get_product_info(elem=product_element, index=website_index)
                    product_dataframe = product_dataframe.append(product_info, ignore_index=True)

                execution_time = time.time() - page_start_time

                print(f'Page {page} - Execution time: {execution_time:.1f}s')
                total_execution_time += execution_time

                if len(next_page_button):
                    driver.execute_script("arguments[0].click();", next_page_button[0])  # or botao[0].click()
                    time.sleep(random.uniform(3, 8))  # Need to change
                    page += 1
                else:
                    break
            print(f'Total execution time: {total_execution_time:.1f}s\n')

            # Create the template of pprice table
            pprice_to_database = pd.DataFrame(columns=[
                'id', 'id_product', 'id_website', 'credit_card', 'cash', 'date'
            ])

            # Create the template of product table
            product_to_database = pd.DataFrame(columns=[
                'id', 'id_maincat', 'id_subcat', 'id_brand', 'description'
            ])

            print('Checking for duplicates in the database...')
            for index, product_scraped in product_dataframe.iterrows():
                # Check if brand exists
                if product_scraped['Brand'] not in list(brand_table['name']):
                    brand_uuid = uuid.uuid4()
                    new_brand = pd.DataFrame({'id': [brand_uuid], 'name': [product_scraped['Brand']]})
                    brand_table = brand_table.append({
                        'id': brand_uuid,
                        'name': product_scraped['Brand']
                    }, ignore_index=True)
                    new_brand.to_sql(name='brand', con=connection, if_exists='append', index=False)

                # Check if the product already exists in product table
                if product_scraped['Description'] in list(product_table['description']):

                    # Create the UUID for pprice table
                    new_id = uuid.uuid4()

                    # Get id_product from product table
                    id_product = product_table['id'].loc[
                        product_table['description'] == product_scraped['Description']
                    ].values[0]

                    # Get id_website from product table
                    id_website = website_table['id'].loc[
                        website_table['name'] == product_scraped['Website']
                    ].values[0]

                    if id_product in pprice_table:
                        continue
                    else:
                        pprice_to_database = pprice_to_database.append({
                            'id': new_id,
                            'id_product': id_product,
                            'id_website': id_website,
                            'credit_card': float(product_scraped['CreditCard']),
                            'cash': float(product_scraped['Cash']),
                            'date': product_scraped['Date']
                        }, ignore_index=True)

                else:
                    # Create the UUID for product table
                    new_product_id = uuid.uuid4()

                    # Get id_maincat
                    id_maincat = maincat_table['id'].loc[
                        maincat_table['name'] == main_category
                    ].values[0]

                    # Get id_subcat
                    id_subcat = subcat_table['id'].loc[
                        subcat_table['name'] == sub_category
                    ].values[0]

                    # Get id_brand
                    id_brand = brand_table['id'].loc[
                        brand_table['name'] == product_scraped['Brand']
                    ].values[0]

                    product_to_database = product_to_database.append({
                        'id': new_product_id,
                        'id_maincat': id_maincat,
                        'id_subcat': id_subcat,
                        'id_brand': id_brand,
                        'description': product_scraped['Description']
                    }, ignore_index=True)

                    # Create the UUID for pprice table
                    new_pprice_id = uuid.uuid4()

                    # Get id_website from product table
                    id_website = website_table['id'].loc[
                        website_table['name'] == product_scraped['Website']
                    ].values[0]

                    if new_product_id in pprice_table:
                        continue
                    else:
                        pprice_to_database = pprice_to_database.append({
                            'id': new_pprice_id,
                            'id_product': new_product_id,
                            'id_website': id_website,
                            'credit_card': float(product_scraped['CreditCard']),
                            'cash': float(product_scraped['Cash']),
                            'date': product_scraped['Date']
                        }, ignore_index=True)

            print(f'Inserting product\'s data into the database...')
            if not product_to_database.empty:
                product_to_database = product_to_database.drop_duplicates()
                product_to_database.to_sql(name='product', con=connection, if_exists='append', index=False)

            print(f'Inserting price\'s data into the database...')
            if not pprice_to_database.empty:
                pprice_to_database = pprice_to_database.drop_duplicates()
                pprice_to_database.to_sql(name='pprice', con=connection, if_exists='append', index=False)
driver.quit()
