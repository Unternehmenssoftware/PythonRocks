import requests

#load data
url='https://raw.githubusercontent.com/Datenschule/schulscraper-data/master/schools/berlin.json'
data=requests.get(url).json()

#delete last entry
del data[-1]

#filter out the id,adress,school_type_entity
schools = []
for art in data:
    schools.append([art['id'],art['address'],art['school_type_entity']])
    
#filter out the adress
adress = []
for key in data:
    adress.append(key['address'])

#split the adress
adress_split = []    
for entry in adress:    
    adress_split.append(entry.split(','))

#filter out the plz
plz_list = []
for plz in adress_split:
    plz_list.append(plz[1])

#delete the first space    
plz_list = [i.strip(' ') for i in plz_list]

#delete the unknown data
for k in plz_list:
    if k == 'undefined Berlin':
        plz_list.remove('undefined Berlin')
#delete some data, that actually doesn't exist       
del plz_list[1028]        

#count all the different plz
counter=set(plz_list)
result={}
for x in counter:
    result[x] = plz_list.count(x)