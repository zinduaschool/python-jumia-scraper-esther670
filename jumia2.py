import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

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

print(brand_list)
print(productname_list)
print(price_list)
print(stock_list)
print(discount_list)
print(rating_list)
print(review_list)
   

with open('jumiaproducts.csv', 'w', newline = '') as jumiafile:
    writer = csv.writer(jumiafile)
    writer.writerow([brand, productname, price_tag, discount, rating, review])
    for i in range(len(brand_list)):
        writer.writerow([
            brand_list[i],
            productname_list[i],
            price_list[i],
            discount_list[i],
            rating_list[i],
            stock_list[i],
            review_list[i]
            ])
    print("Done! All products have been added to CSV file")

df = pd.read_csv('jumiaproducts.csv', encoding='unicode escape')
print(df.head(10))


numratings = []
for rating in rating_list:
    if rating != 'No rating':
        numratings.append(float(rating.split(' ')[0])) 
    else:
        numratings.append(0.0)
print(numratings)

numreviews =[]
for review in review_list:
    if review!= 'No reviews':
        newreview= re.findall(r'\d+',review)
        newreview=int(newreview[-1])
        numreviews.append(newreview)
    else:
        numreviews.append(0.0)
print(numreviews)


popularity_score = numratings * numreviews
print(popularity_score)

