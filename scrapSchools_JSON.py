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
    schools.append([art['school_type'],art['school_type_entity'],art['name'],art['address']])

#schools in Dataframe
df = pd.DataFrame(schools, columns=['Category','SubCategory','Name','Adress',])

#split adress ,add PLZ and remove plz out of adress
df['ZipCode'] = df.Adress.str.split(', ').str.get(1)
df['Adress'] = df.Adress.str.split(', ').str.get(0)

#remove 'Berlin'
df['ZipCode'] = df['ZipCode'].str.rstrip(' Berlin')

#delete the unknown data
df = df[df.ZipCode != 'undefined']

#drop column Address
#df = df.drop('Address', 1)

#dataframe ordnen
df = df[['ZipCode', 'Category', 'SubCategory', 'Name', 'Adress']]

#save in Excel
writer = pd.ExcelWriter('scrabSchools_JSON.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Schools', index=False)
worksheet = writer.sheets['Schools']
worksheet.set_column('B:B', 35)
worksheet.set_column('C:C', 35)
worksheet.set_column('D:D', 65)
worksheet.set_column('E:E', 30)
writer.save()
