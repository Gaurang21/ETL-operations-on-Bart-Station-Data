import mysql.connector
import pandas as pd
import os
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1@Safegns@2",
  database="prob1") #connect to database

my_cursor = mydb.cursor(buffered=True) #Buffered= True to handle multiple results and store in a buffer
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
for filename in os.listdir("./"):#access file in current directory
	if filename.endswith(".xlsx"):#excel files
		print(filename)
		df = pd.read_excel(filename,sheet_name="Total Trips OD",skiprows=[0],index_col=0)#read excel files in a dataframe
		#print(df)
		stations = df.columns[0:-1]
		id = filename.lstrip('Ridership_').rstrip('.xlsx') #Get id from the filename
		year = id[0:4] #get year
		month =id[4:] #get month
		for entry_station in stations: #for each entry_station
			for exit_station in stations:	#for each exit_station
				query = "select STATION_ID from T_BART_STATION where CODE=%s" # get entry_station ID
				values = (entry_station,) 
				my_cursor.execute(query,values)
				entry_station_id = my_cursor.fetchone()
				
				query = "select STATION_ID from T_BART_STATION where CODE=%s" # get exit_station ID
				values = (exit_station,)
				my_cursor.execute(query,values)
				exit_station_id = my_cursor.fetchone()

				if entry_station_id==None or exit_station_id==None: #If either ID is None we continue
					continue;
				entry_station_id = entry_station_id[0]
				exit_station_id = exit_station_id[0]
				#print(id,exit_station_id,entry_station_id,df.loc[exit_station,entry_station],year,month)
				# Populate T_RIDERSHIP with appropriate values
				query = "INSERT INTO T_RIDERSHIP(RIDERSHIP_ID,MONTH,YEAR,ENTRY_STATION_ID,EXIT_STATION_ID,COUNT) VALUES(%s,%s,%s,%s,%s,%s)"
				values = (id,month,year,entry_station_id,exit_station_id,int(df.loc[exit_station,entry_station]))
				my_cursor.execute(query,values)
				mydb.commit()

print('success')

