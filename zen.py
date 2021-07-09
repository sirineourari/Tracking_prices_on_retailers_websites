from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import pandas as pd

options = Options()
options.add_argument("--headless")
prefs = {'profile.default_content_setting_values': {
    'images': 2, 'permissions.default.stylesheet': 2, 'javascript': 2}}
options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# dresses,pants,blazers,t-shirts,shoes,accessories
label = ["dresses", "pants", "blazers",
         "t-shirts", "shoes", "accessories"]
categories_zen = ["https://www.zen.com.tn/10-robes", "https://www.zen.com.tn/19-pantalons", "https://www.zen.com.tn/151-gilets",
                  "https://www.zen.com.tn/13-tops-t-shirts", "https://www.zen.com.tn/196-chaussures", "https://www.zen.com.tn/72-accessoires"]
# .replace(u'\xa0', u'')


def scrape_product_page(url):
    driver.get(url)
    time.sleep(1.2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    d0 = soup.find_all('h1', attrs={'class': 'h3 product-title'})
    d1 = soup.find_all('span', attrs={'class': 'price'})
    results = {}

    results['Product'] = []
    results['Price'] = []
    for (product, price) in zip(d0, d1):
        results['Product'].append(product.text)
        results['Price'].append(price.text)
    return(results)


categories_res = []
for url in categories_zen:
    #res = {}
    # print(url)
    res = scrape_product_page(url)
    # print(res)
    categories_res.append(res)
# print(categories_res)


list_dataframes = []
i = 0
for cat in categories_res:
    category_df = pd.DataFrame(cat)
    category_df['category'] = label[i]
    i += 1
    list_dataframes.append(category_df)
complete_dataframe = pd.DataFrame()
complete_dataframe = pd.concat(list_dataframes)
print(complete_dataframe.head())
complete_dataframe.to_csv("output.csv", index=False)
