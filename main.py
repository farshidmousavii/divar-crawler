import requests

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




    
