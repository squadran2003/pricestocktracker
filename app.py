from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


# get the number of pages for this category
url = "https://www.amazon.co.uk/Best-Sellers-Books/zgbs/books/ref=zg_bs_nav_0"
result = requests.get(url)
# zg-ordered-list
src = result.content

soup = BeautifulSoup(src, 'lxml')

ul = soup.find('ul', {'class': 'a-pagination'})
pages = len(ul.find_all('li',{'class':["a-selected","a-normal"]}))


print("Amazon best selling books!")
data = []
# get books for each page and store in a list
for num in range(1,pages+1):
    url = "https://www.amazon.co.uk/Best-Sellers-Books/zgbs/books/ref=zg_bs_pg_{}?_encoding=UTF8&pg={}".format(num,num)
    result = requests.get(url)
    src = result.content
    soup2 = BeautifulSoup(src, 'lxml')
    lis = soup2.find_all('li',{'class':"zg-item-immersion"})
    for i in lis:
        price = "unknown"
        links = i.find("a", {'class':"a-link-normal"})
        item_name = links.find_all('div')
        product_name = item_name[len(item_name)-1].text
        price =  i.find("span", {'class':"p13n-sc-price"})
        item_name = str(product_name).strip()
        if price:
            price = str(price.text).replace("£","")
        data.append(
            {
            'Item name':item_name,
            'price':price
            }

        )
    time.sleep(1)
# store results in a pandas data frame
data = pd.DataFrame(data)
print(data)

