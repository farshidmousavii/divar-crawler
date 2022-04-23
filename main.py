import requests
from bs4 import BeautifulSoup
import csv

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

    if count >= 200 :
        break

with open ("token.txt" , "w" , encoding="utf8") as file :
    file.write(",".join(list_of_tokens))


url_list = [ f"https://divar.ir/v/-/{token}" for token in list_of_tokens]

for url in url_list :
    response = requests.get(url)
    soup = BeautifulSoup(response.content , "html.parser")
    information = soup.find_all("span" , class_="kt-group-row-item__value")
    price = soup.find_all("p" , class_ ="kt-unexpandable-row__value")
    deposit = price[0].getText()
    rent = price[1].getText()
    area = information[0].getText()
    construction =   information[1].getText()
    rooms = information[2].getText()
    elevator = False if "ندارد" in information[3].getText() else True
    pariking = False if "ندارد" in information[4].getText() else True
    warehouse = False if "ندارد" in information[5].getText() else True

    
    with open ("result.csv" , "w") as file :
        wirter = csv.writer(file)
        wirter.writerow(row=["deposit",
                        "rent",
                        "area",
                        "construction",
                        "rooms",
                        "elevator",
                        "pariking",
                        "warehouse"])
        wirter.writerows(row=[deposit,
                        rent,
                        area,
                        construction,
                        rooms,
                        elevator,
                        pariking,
                        warehouse,])