import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("liqourpenn@gmail.com", "wvumhs12") 
message = """From: liqourpenn@gmail.com\nTo: pawineliquor@gmail.com\nSubject: NewBeverageAlert\n"""


BASE_URL = "https://www.finewineandgoodspirits.com"


headers = {
    'Connection': 'keep-alive',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'https://www.finewineandgoodspirits.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334015&variety=Bourbon&categoryType=Spirits&parent_category_rn=1334013&searchSource=E&sortBy=5&top_category=25208&pageView=&beginIndex=0',
    'Accept-Language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    ('langId', '-1'),
    ('storeId', '10051'),
    ('catalogId', '10051'),
    ('advancedSearch', ''),
    ('sType', 'SimpleSearch'),
    ('categoryId', '1334015'),
    ('searchType', '1002'),
    ('facet', ''),
    ('searchTermScope', ''),
    ('searchTerm', ''),
    ('metaData', ''),
    ('resultCatEntryType', ''),
    ('filterFacet', ''),
    ('manufacturer', ''),
    ('emsName', ''),
    ('gridPosition', ''),
    ('resultsPerPage', '45'),
    ('minPrice', ''),
    ('maxPrice', ''),
    ('sortBy', '5'),
    ('disableProductCompare', 'false'),
    ('ajaxStoreImageDir', '/wcsstore/WineandSpirits/'),
    ('filterTerm', ''),
    ('variety', 'Bourbon'),
    ('categoryType', 'Spirits'),
    ('enableSKUListView', ''),
    ('ddkey', 'ProductListingView'),
)

data = {
  'contentBeginIndex': '0',
  'productBeginIndex': '0',
  'beginIndex': '0',
  'orderBy': '',
  'facetId': '',
  'pageView': '',
  'resultType': 'products',
  'orderByContent': '',
  'searchTerm': '',
  'facet': '',
  'facetLimit': '',
  'minPrice': '',
  'maxPrice': '',
  'pageSize': '',
  'storeId': '10051',
  'catalogId': '10051',
  'langId': '-1',
  'categoryId': '1334015',
  'objectId': '',
  'requesttype': 'ajax'
}

response = requests.post('https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CategoryProductsListingView', headers=headers, params=params, data=data)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CategoryProductsListingView?langId=-1&storeId=10051&catalogId=10051&advancedSearch=&sType=SimpleSearch&categoryId=1334015&searchType=1002&facet=&searchTermScope=&searchTerm=&metaData=&resultCatEntryType=&filterFacet=&manufacturer=&emsName=&gridPosition=&resultsPerPage=15&minPrice=&maxPrice=&sortBy=5&disableProductCompare=false&ajaxStoreImageDir=%2fwcsstore%2fWineandSpirits%2f&filterTerm=&variety=Bourbon&categoryType=Spirits&enableSKUListView=&ddkey=ProductListingView', headers=headers, cookies=cookies, data=data)






# r = requests.get("https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334015&variety=Bourbon&categoryType=Spirits&parent_category_rn=1334013&searchSource=E&sortBy=5&top_category=25208&pageView=&beginIndex=0#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:45&")
# r1 = requests.get("https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334015&variety=Bourbon&categoryType=Spirits&parent_category_rn=1334013&searchSource=E&sortBy=5&top_category=25208&pageView=&beginIndex=0#facet:&productBeginIndex:0&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:&")
# r2 = requests.get("https://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/CatalogSearchResultView?storeId=10051&catalogId=10051&langId=-1&categoryId=1334015&variety=Bourbon&categoryType=Spirits&parent_category_rn=1334013&searchSource=E&sortBy=5&top_category=25208&pageView=&beginIndex=0#facet:&productBeginIndex:15&orderBy:&pageView:&minPrice:&maxPrice:&pageSize:&")


with open('itemlist.txt', 'r') as f:
    itemList = [line.strip() for line in f]

# soup1 = BeautifulSoup(r1.content, "html.parser")
# soup2 = BeautifulSoup(r2.content, "html.parser")
# namelist1 = soup1.find_all("a", class_="catalog_item_name", attrs={"aria-hidden": "true", "tabindex": "-1"})
# namelist2 = soup2.find_all("a", class_="catalog_item_name", attrs={"aria-hidden": "true", "tabindex": "-1"})
# newlist = namelist1 + namelist2

soup = BeautifulSoup(response.content, "html.parser")
newlist = soup.find_all("a", class_="catalog_item_name", attrs={"aria-hidden": "true", "tabindex": "-1"})


blahlist = []
print(itemList)
with open("itemlist.txt", 'a') as itemfile:
    for item in newlist:
        link = item["href"]
        if link in itemList:
            pass
        else:
            if link in blahlist:
                pass
            else:
                newlink = BASE_URL + link
                print(newlink)
                itemfile.write(link + "\n")
                x = f"\n{item.text}:\n{newlink}\n\n"
                message = message + x
                print("ITEM NOT IN LIST: ", item.text)
                blahlist.append(link)

if len(blahlist) > 0:
    s.sendmail(from_addr="liqourpenn@gmail.com", to_addrs="pawineliquor@gmail.com", msg=message )