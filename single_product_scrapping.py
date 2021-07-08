from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

options=Options()
options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install( ), options=options)

url="https://www.zara.com/tn/fr/gilet-sans-manches-%C3%A0-coutures-contenant-du-lin-p02010700.html?v1=110260001&v2=1718076"
title_lookup= "#productTitle"
price_lookup="#priceblock_ourprice"

driver.get(url)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
d0 = soup.find_all('h1', attrs={'class': 'product-detail-info__name'})
d1 = soup.find_all('span', attrs={'class': 'price__amount-current'})

results = {}
for (agency, rate) in zip(d0, d1):
    results[agency.text] = (rate.text).replace(u'\xa0', u'')
print(results)


