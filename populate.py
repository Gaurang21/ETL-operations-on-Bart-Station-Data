import mysql.connector
import ssl
import pandas as pd
import urllib.request as ur

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1@Safegns@2",
  database="prob1") # connect to database

my_cursor = mydb.cursor(buffered=True)# cursor to the database 

tables=my_cursor.execute("show databases")
'''
for db in my_cursor:
	print(db)
'''
my_cursor.execute("use prob1")
my_cursor.execute("show tables")

'''
for tables in my_cursor:
	print(tables)
'''
#create context for ssl certificate to access the site
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url="https://www.bart.gov/sites/default/files/docs/Station_Names.xls"# retrieve file

file_ = ur.urlopen(url,context=ctx) 
with open("Station_Names.xls","wb") as fl: # Store data in excel file
	fl.write(file_.read())

df = pd.read_excel('Station_Names.xls') # Read excel file in a dataframe

for i in range(len(df)): #populate database 
	query = "INSERT INTO T_BART_STATION(STATION_ID,NAME,CODE) VALUES(%s,%s,%s)"
	values = (i+1,df["Station Name"][i],df["Two-Letter Station Code"][i])
	my_cursor.execute(query, values)
	mydb.commit()
	#print(my_cursor.rowcount,' records inserted')
print('success')
