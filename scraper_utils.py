from selenium.webdriver.chrome.options import Options
import variables
from datetime import date


def set_options():
    option_list = variables.driver_options_list

    driver_options = Options()
    for option_name in option_list:
        driver_options.add_argument(option_name)

    return driver_options


def get_product_info(elem, index):
    website = list(variables.websites.keys())[list(variables.websites.values()).index(index)]
    description = elem.find_element_by_xpath(variables.xpaths['Description'][index]).text
    brand = elem.find_element_by_xpath(variables.xpaths['Brand'][index]).get_attribute('alt')
    credit_card = elem.find_element_by_xpath(variables.xpaths['CreditCard'][index]).text
    cash = elem.find_element_by_xpath(variables.xpaths['Cash'][index]).text

    product_info = {
        'Website': website,
        'Description': description,
        'Brand': brand,
        'CreditCard': credit_card,
        'Cash': cash,
        'Date': date.today()
    }

    return product_info
