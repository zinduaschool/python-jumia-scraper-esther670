import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
mainurl = 'https://jumia.co.ke/'
url = 'https://www.jumia.co.ke/flash-sales/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
           "Accept-Language": "en-US, en;q=0.5"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup (response.text, 'html.parser')
print(response)


productinfo = soup.find_all('article',{'class':'prd _fb _p col c-prd'})

brand_list=[]
productname_list=[]
price_list=[]
discount_list=[]
rating_list=[]
stock_list=[]
review_list =[]

for products in productinfo:
    brand = products.find('a', {'class':'core'})['data-gtm-brand']
    productname = products.find('h3',{'class':'name'}).text
    price_tag = products.find('div',{'class':'prc'}).text
    discount_item = products.select_one('div.bdg._dsct')
    discount = discount_item.text if discount_item else "No discount"
    rating_item = products.find('div',{'class':'stars _s'})
    rating = rating_item.text if rating_item else "No rating"
    stock = products.find('div',{'class':'stk'}).text
    review_item = products.find('div', {'class':'rev'})
    review = review_item.text[-3:15] if review_item else "No reviews"
    
    
    brand_list.append(brand)
    productname_list.append(productname)
    price_list.append(price_tag)
    discount_list.append(discount)
    rating_list.append(rating)
    stock_list.append(stock)
    review_list.append(review)

df = pd.DataFrame({
        'Brand': brand_list,
        'Product Name': productname_list,
        'Price': price_list,
        'Discount': discount_list,
        'Rating': rating_list,
        'Stock': stock_list,
        'Review': review_list
    })

df['Price'] = df['Price'].str.replace('KSh', '').str.replace(',', '').astype(float)
df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
df['Review'] = df['Review'].str.extract(r'(\d+)').astype(float)

df['Popularity Score'] = df['Rating'] * df['Review']

df.sort_values(by='Popularity Score', ascending=False, inplace=True)

df.to_csv('jumiaproducts2.csv', index=False)
print("Done! All products have been added to the CSV file.")