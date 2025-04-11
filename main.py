from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re
import os

# Initialize WebDriver
driver = webdriver.Firefox()

# Open Amazon
driver.get("https://www.ebay.com")
time.sleep(5)  # Let the page load
wait = WebDriverWait(driver, 100)

product_input = input("type the product you want to search?  ")
page_counter = int(input("how many page you want to extract? "))
elem = driver.find_element(By.ID, "gh-ac")
elem.clear()
elem.send_keys(product_input)
elem.send_keys(Keys.RETURN)

if not os.path.exists("./images"):  
    os.mkdir("./images")

header = {"product name":"product name",
           "product price":"product price",
            "delivery cost":"Delivery cost"
            "product condition": "product condition",
            "product image path": "product image"
            "product from": "product from"}
            
df = pd.DataFrame([header])
df.to_csv(f'Data.csv',  mode='a', header=False, index=False)


product_title = []
product_condition = []
product_price = []
product_location = []
shipping_cost = []


def extract_page(page):
    global product_title, product_condition, product_price
    
    print(f"Extracting page {page} information...")
    product_display_area = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".srp-results.srp-list.clearfix")))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    product_display_section = soup.find("ul",class_=["srp-results","srp-list", "clearfix"])

    product_section = product_display_section.find_all("li",class_=["s-item", "s-item__pl-on-bottom"])
    #print(len(product_section))

    
    for product_listing in product_section:
        product_discription_title = product_listing.find("div",class_=["s-item__title"])
        product_title.append(product_discription_title.find("span").text.strip())
    
        product_price.append(product_listing.find("span",class_="s-item__price").text.strip())

        product_image_container = product_listing.find("div",class_="s-item__image-wrapper image-treatment")
        image = product_image_container.find('img')
        response = requests.get(image.get('src'))
        image_name = product_discription_title.find("span").text.strip()
        clean_name = re.sub(r'[^A-Za-z0-9 ]+', '', product_discription_title.find("span").text.strip()) 
        
        delivery = product_listing.find("span",class_="s-item__shipping s-item__logisticsCost").text.strip()
        shipping_cost.append(delivery.split()[0])
        with open(f"./images/{clean_name}.jpg", 'wb') as f:
                f.write(response.content)
        
        try:
        
            product_condition_page = product_listing.find_all("div",class_="s-item__subtitle")
            
            if len(product_condition_page) == 1:
                product_condition.append(product_condition_page[0].find("span",class_="SECONDARY_INFO").text.strip())
                product_location.append(product_listing.find("span",class_="s-item__location s-item__itemLocation").text.strip())
            elif product_condition_page == None:
                sideline_product_condition_page = product_listing.find("div",class_="s-item__dynamic s-item__normalizedCondition")
                product_condition.append(sideline_product_condition_page.find("span",class_="SECONDARY_INFO").text.strip())
                product_location.append("unspecified")
            else:
                product_condition.append(product_condition_page[1].find("span",class_="SECONDARY_INFO").text.strip())
                product_location.append(product_listing.find("span",class_="s-item__location s-item__itemLocation").text.strip())
            
        
           
        except Exception as e:
            sideline_product_condition_page = product_listing.find("span",class_="s-item__dynamic s-item__normalizedCondition")
            product_condition.append(sideline_product_condition_page.find("span",class_="SECONDARY_INFO").text.strip())
            product_location.append("unspecified")
        
            print("side line products appear")
        
        product_info = {"product title":str(product_discription_title.find("span").text.strip()),
                        "product price":str(product_listing.find("span",class_="s-item__price").text.strip()),
                        "delivery cost":shipping_cost[-1],
                        "product condition":product_condition[-1],
                        "product image name":"./images/"+clean_name+".jpg",
                        "product location":product_location[-1]}
                        
        
        df = pd.DataFrame([product_info])
        df.to_csv(f'Data.csv',  mode='a', header=False, index=False)
    

    print(len(product_title),len(product_location),len(shipping_cost))
    print(f" page {page} {len(product_condition)} product information saved to CSV file.")   
    product_condition.clear()
    product_title.clear()
    product_price.clear() 
        

        

    time.sleep(5)  # See the effect

    paginate = driver.find_element(By.CSS_SELECTOR, ".pagination__next.icon-link")
    paginate.click()
    
    #next_page = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".srp-results.srp-list.clearfix")))
    time.sleep(5)
    
    

for page in range(1,page_counter+1):
        
    
    extract_page(page)     
driver.quit()
