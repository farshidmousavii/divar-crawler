import requests
from bs4 import BeautifulSoup
import pandas as pd



url = "https://api.divar.ir/v8/search/1/residential-rent"
json = {"json_schema":{"category":{"value":"residential-rent"},"districts":{"vacancies":["195","654"]}},"last-post-date":1650519315954570}
headers = {"Content/type" : "application/json"}
response = requests.post(url , json=json , headers=headers )
data = response.json()
last_post_date = data["last_post_date"]

list_of_tokens =[]
count = 0
while True :
    json = {"json_schema":{"category":{"value":"residential-rent"},"districts":{"vacancies":["195","654"]}},"last-post-date":last_post_date}
    response = requests.post(url , json=json , headers=headers )
    data = response.json()
    last_post_date = data["last_post_date"]

    for widget in data["widget_list"] :
        token = widget["data"]["token"]
        list_of_tokens.append(token)
        count += 1
        if count >= 10 :
            break   
        print(count)
    if count >= 10 :
        break   


with open ("token.txt" , "w" , encoding="utf-8") as file :
    file.write(",".join(list_of_tokens))


url_list = [ f"https://divar.ir/v/-/{token}" for token in list_of_tokens]

result = []
n =1
for url in url_list :
    response = requests.get(url)
    soup = BeautifulSoup(response.content , "html.parser")
    information = soup.find_all("span" , class_="kt-group-row-item__value")
    price = soup.find_all("p" , class_ ="kt-unexpandable-row__value")
    desciption = soup.find("p" , class_ = "kt-description-row__text post-description kt-description-row__text--primary").getText()
    deposit = price[0].getText()
    rent = price[1].getText()
    area = information[0].getText()
    construction =   information[1].getText()
    rooms = information[2].getText()
    elevator = False if "ندارد" in information[3].getText() else True
    pariking = False if "ندارد" in information[4].getText() else True
    warehouse = False if "ندارد" in information[5].getText() else True

    result.append({
        "deposit": deposit,
        "rent" : rent ,
        "area" : area ,
        "construction" : construction,
        "rooms" : rooms ,
        "elevator" : elevator ,
        "pariking" : pariking ,
        "warehouse" : warehouse,
        "desciption" : desciption,
    })
    print ( n ,f"Crawling {url}" )
    n +=1
df = pd.DataFrame(result)
df.to_csv("result.csv" , encoding="utf-8-sig")   


    
