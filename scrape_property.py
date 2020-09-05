import requests
import bs4, re
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("mandalamit71@gmail.com", "akmandal") 
  


currentDate = datetime.datetime.now()
day = currentDate.day
month = currentDate.month
year = currentDate.year

cookies = {
    'sortField': 'Document+Id',
    'sortDir': 'asc',
    'pageSize': '51',
    'isLoggedInAsPublic': 'true',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://or.occompt.com',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://or.occompt.com/recorder/eagleweb/docSearch.jsp',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = {
  'RecordingDateIDStart': f"{month}/04/{year}r",
  'RecordingDateIDEnd': '',
  'BothNamesIDSearchString': '',
  'BothNamesIDSearchType': 'Exact Match',
  'GrantorIDSearchString': '',
  'GrantorIDSearchType': 'Exact Match',
  'GranteeIDSearchString': '',
  'GranteeIDSearchType': 'Exact Match',
  'DocumentID': '',
  'BookPageIDBook': '',
  'BookPageIDPage': '',
  'PLSSIDSixtyFourthSection': '',
  'PLSSIDSection': '',
  'PLSSIDTownship': '',
  'PLSSIDRange': '',
  'PlattedIDLot': '',
  'PlattedIDBlock': '',
  'PlattedIDTract': '',
  'PlattedIDUnit': '',
  'CaseID': '',
  'DeedDocTaxStart': '7000',
  'DeedDocTaxEnd': '',
  'MortgageDocTaxStart': '',
  'MortgageDocTaxEnd': '',
  'IntangibleTaxStart': '',
  'IntangibleTaxEnd': '',
  'ParcelID': '',
  'LegalRemarks': '',
  'AllDocuments': 'ALL',
  'docTypeTotal': '41'
}

response = requests.post('https://or.occompt.com/recorder/eagleweb/docSearchPOST.jsp', headers=headers, cookies=cookies, data=data)
print(response.content, file=open('abc.html', "w"))
soup = bs4.BeautifulSoup(response.content, "lxml")
neededtags = soup.find_all(text=re.compile("Add to My Images"))
needed = divs = [score.parent.parent for score in neededtags]
print("Number of entries collected: " + str(len(needed)))


# message to be sent 
message = """From: mandalamit71@gmail.com\nTo: bilbobaggins20711@gmail.com\nSubject: ScrapedData\n"""

for item in needed:
  x = str(item)
  # result = re.search("jsp?docName=(.*)&amp;id=", x)
  # id1, id2 = result.group(1), result.group(2)
  # print(result.group(1))
  docName = x[x.find("jsp?docName=")+len("jsp?docName="):x.rfind("&amp;id")]
  _id = x[x.find("&amp;id=")+len("&amp;id="):x.rfind(".A0&amp;parent=")]
  x = x.split("&amp;parent=")[1]
  parentid = x.split('" oid="')[0]
  # print(f"https://or.occompt.com/recorder/eagleweb/downloads/{docName}?id={_id}.A0&parent={parentid}&preview=false&noredirect=true")
  x = f"\nhttps://or.occompt.com/recorder/eagleweb/downloads/{docName}?id={_id}.A0&parent={parentid}&preview=false&noredirect=true" + "\n"
  message = message + x


print(message)
s.sendmail(from_addr="mandalamit71@gmail.com", to_addrs="bilbobaggins20711@gmail.com", msg=message )
print("Email Sent")

s.quit() 