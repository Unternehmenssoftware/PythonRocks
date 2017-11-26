import requests
import pandas as pd
from bs4 import BeautifulSoup

#url='https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Umkreissuche/Berlin/10369/231837/2513303/-/-/1?enteredFrom=one_step_search'
#r=requests.get(url)

#soup = BeautifulSoup(r.text)
#soup.prettify()
#csvfile="dataoutput.csv"

#links=soup.find_all("a")

zipCode = []
title = []
address = []
district = []
neighboorhood = []
coldrent = []
squaremeter = []
rooms = []

for page in range(1,200):
    if page==1:
        url='https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin?enteredFrom=one_step_search'

    url='https://www.immobilienscout24.de/Suche/S-T/P-'+ str(page) +'/Wohnung-Miete/Berlin/Berlin'
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'lxml')
    result_xl_bool = True
    #if result_xl_bool:
     #   dataset=soup.find_all("li", {"class:", "result-list__listing result-list__listing--xl"})
    #else:
     #   dataset=soup.find_all("li", {"class:", "result-list__listing "})
        
    dataset=soup.find_all("li")
    
    print(page)

    for data in dataset:
        try:
            expose_ID=(data.get('data-id'))
            #expose_ID=((data.find_all('a')[0]).get('href').split('/'))[2]
            if expose_ID == "www.immobilienscout.de":
                continue
            else:
                url = 'https://www.immobilienscout24.de/Suche/controller/exposeNavigation/goToExpose.go?exposeId=' + expose_ID + '&searchUrl=%2FSuche%2FS-T%2FWohnung-Miete%2FBerlin%2FBerlin&referrer=RESULT_LIST_LISTING&hasNext=true&hasPrev=true'
                r=requests.get(url)
                soup=BeautifulSoup(r.text, 'lxml')
                zipCode.append(((soup.find_all("span", {"class:", "zip-region-and-country"})[0].text).split(" "))[1])
                
                try:
                    preaddress=data.contents[0].find_all("div", {"class:", "result-list-entry__address"})[0].text
                    
                    if preaddress.count(",") == 1:
                        preaddress= "a , "+preaddress
                    address_1=preaddress.split(",")
                    if (len(address_1[0])<=2):
                        address.append("Null")
                    else:
                        address.append(address_1[0])
                except:
                    pass
                try:    
                    predistrict=address_1[1].split("(")
                    if (len(predistrict[0])==0):
                        neighboorhood.append("Null")
                    else:
                        neighboorhood.append(predistrict[0])
                except:
                    pass
                try:    
                    if predistrict[1] is None:
                        district.append(neighboorhood)
                    else:
                        district.append((predistrict[1])[:-1])
                except IndexError:
                    district.append("ERROR---ERROR---ERROR")
                    pass
                try:    
                    precoldrent=data.contents[0].find_all("dd",{"class:","font-line-xs"})[0].text
                    if len(precoldrent[0])==0:
                        coldrent.append("Null")
                    else:
                        coldrent.append(str(precoldrent[:-2]))
                except:
                    pass
                try:
                    presquaremeter=data.contents[0].find_all("dd",{"class:","font-line-xs"})[1].text
                    if len(presquaremeter[0])==0:
                        squaremeter.append("Null")
                    else:
                        squaremeter.append(str(presquaremeter[:-3]))
                except:
                    pass
                try:    
                    prerooms=data.contents[0].find_all("dd",{"class:","font-line-xs"})[2].text
                    if len(prerooms[0])==0:
                        prerooms=data.contents[0].find_all("dd",{"class:","font-line-xs"})[2].text
                    if (len(prerooms)==0):
                        rooms.append("Null")
                    else:
                        rooms.append(str(prerooms))
                    
                    #print(rooms)
                except:
                    pass
        except:
            pass
    result_xl_bool=False
    
        
df=pd.DataFrame({'Zip Code': zipCode,
                 'Address': address,
                 'Neighborhood': neighboorhood,
                 'District': district,
                 'Coldrent': coldrent,
                 'Squaremeter': squaremeter,
                 'Rooms': rooms})
df['Coldrent'].unique   
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Immo', index=False)
writer.save()   

xl=pd.ExcelFile('output.xlsx')
df2=xl.parse('Immo')

for e in df2:
    if e not in df:
        df.append(e)
        
print(df)
df.to_excel(writer,'Immo', index=False)
writer.save








