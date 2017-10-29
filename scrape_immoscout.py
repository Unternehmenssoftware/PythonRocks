import requests
from bs4 import BeautifulSoup

url='https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Umkreissuche/Berlin/10369/231837/2513303/-/-/1?enteredFrom=one_step_search'
r=requests.get(url)

soup = BeautifulSoup(r.text)
soup.prettify()

links=soup.find_all("a")

for link in links:
    print("<a href='%s'>%s</a>" %(link.get("href"), link.text))
    
dataset=soup.find_all("div", {"class:", "grid-item result-list-entry__data-container"})

for data in dataset:
    #print(data.contents[0].text)
    try:
        title=data.contents[0].find_all("h5", {"class:", "result-list-entry__brand-title font-h6 onlyLarge nine-tenths font-ellipsis"})[0].text
        print(title)
    except:
        pass
    try:
        address=data.contents[0].find_all("div", {"class:", "result-list-entry__address"})[0].text
        #address_1=address.split()
        #address_2=address_1[0]+" "+(address_1[1])[:-1]
        #print(address_2)
        #print(address_1[2])
        #print((address_1[3])[1:-2])
        address_1=address.split(",")
        print(address_1[0])
        address_2=address_1[1].split("(")
        print((address_2[0])[1:-1])
        print((address_2[1])[:-1])
    except:
        pass
    try:
        kaltmiete=data.contents[0].find_all("dd",{"class:","font-nowrap font-line-xs"})[0].text
        print(kaltmiete[:-2])
    except:
        pass
    try:
        flaeche=data.contents[0].find_all("dd",{"class:","font-nowrap font-line-xs"})[1].text
        print(flaeche[:-3])
    except:
        pass
    try:
        zimmer=data.contents[0].find_all("dd",{"class:","font-nowrap font-line-xs"})[2].text
        print(zimmer)
    except:
        pass
    
    print() 








