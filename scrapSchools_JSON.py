import requests
import pandas as pd

#load data
url='https://raw.githubusercontent.com/Datenschule/schulscraper-data/master/schools/berlin.json'
data=requests.get(url).json()

#delete last entry
del data[-1]

#filter out the id,adress,school_type_entity
schools = []
for art in data:
    schools.append([art['id'],art['address'],art['school_type_entity']])


#schools in Dataframe
df = pd.DataFrame(schools, columns=['ID','Address','School_type'])

#split address to PLZ
df['PLZ'] = df.Address.str.split(', ').str.get(1)

#remove 'Berlin'
df['PLZ'] = df['PLZ'].str.rstrip(' Berlin')

#delete the unknown data
df = df[df.PLZ != 'undefined']

#drop column Address
df = df.drop('Address', 1)

#save in Excel
writer = pd.ExcelWriter('scrabSchools_JSON.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Schools', index=False)
worksheet = writer.sheets['Schools']
worksheet.set_column('B:B', 35)
writer.save()
