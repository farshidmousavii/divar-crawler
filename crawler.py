import scrapy

url = "https://divar.ir/v/-/{token}"
with open ("token.txt" , "r") as file :
        tokens = file.read().split(",")



class DivarSpider (scrapy.Spider) :

    name = "divar"
    start_urls = [url.format(token=token) for token in tokens ]
    

    def parse(self , response) :
        information = response.css('div span.kt-group-row-item__value::text')
        price = response.css("div p.kt-unexpandable-row__value::text")
        description = response.css("div p.kt-description-row__text--primary::text").extract()
        deposit = price[0].extract()
        rent =price[1].extract()
        area = information[0].extract().encode("utf-8-sig")
        construction =   information[1].extract()
        rooms = information[2].extract()
        elevator = False if "ندارد" in information[3].extract() else True
        pariking = False if "ندارد" in information[4].extract() else True
        warehouse = False if "ندارد" in information[5].extract() else True

        
        yield {
        "deposit": deposit,
        "rent" : rent ,
        "area" : area ,
        "construction" : construction,
        "rooms" : rooms ,
        "elevator" : elevator ,
        "pariking" : pariking ,
        "warehouse" : warehouse,
        "description" : description,
        }
