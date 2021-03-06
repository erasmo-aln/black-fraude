import time
from datetime import date

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import variables
import scraper_utils


# Initialize chromedriver with predefined options
chrome_options = scraper_utils.set_options()
driver = webdriver.Chrome(options=chrome_options)

for website_name, website_index in variables.websites.items():
    for main_category, sub_categories_list in variables.categories.items():
        for sub_category in sub_categories_list:

            # Reset these for each loop
            page = 1
            total_execution_time = 0
            link = variables.links[sub_category][website_index]
            products_dataframe = pd.DataFrame(variables.product_dataframe)

            print(f'\n{website_name} - {main_category} - {sub_category}:')

            driver.get(link)
            time.sleep(1)

            # Looping through pages
            while True:
                page_start_time = time.time()

                # Get all page's products
                next_page_button = driver.find_elements_by_xpath(variables.xpaths['NextPage'][website_index])
                products_list = driver.find_elements_by_xpath(variables.xpaths['Products'][website_index])

                # Looping through products
                for product_element in products_list:

                    # Add the 'product_info' dictionary as a row in the dataframe
                    product_info = scraper_utils.get_product_info(elem=product_element, index=website_index)
                    products_dataframe = products_dataframe.append(product_info, ignore_index=True)

                execution_time = time.time() - page_start_time

                print(f'Page {page} - Execution time: {execution_time:.1f}s')
                total_execution_time += execution_time

                if len(next_page_button):
                    driver.execute_script("arguments[0].click();", next_page_button[0]) # or botao[0].click()
                    time.sleep(1)
                    page += 1
                else:
                    break

        #nome_csv = 'data/' + str(categoria) + '.csv'
        #produtos = pd.DataFrame.from_dict(produtos)
        #produtos.to_csv(nome_csv, encoding='utf-8', index=False)
        print(f'Total execution time: {total_execution_time:.1f}s\n')
driver.quit()
