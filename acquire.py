from bs4 import BeautifulSoup
import requests
import urllib.request as ur
from datetime import datetime
import os


base_url = "http://64.111.127.166/ridership/" 
r  = requests.get(base_url) #access website
data = r.text
#print(data)

soup = BeautifulSoup(data, 'html.parser') #parse HTML using Beautiful Soup
a_tag = soup.findAll('a') # a tag contains all the links
#print(a_tag)

#Loop through each a tag
for link in a_tag:
	#print(link)
	href = link.get('href') #get href attribute which contains the file names
	if '.xlsx' in href:
		name = href.rstrip('.xlsx') #Strip xlsx to get the name of file
		#print("'"+name+"'")
		#print(href)
		ur.urlretrieve(base_url+href, name+".xlsx") #retrive each file

metadata=[]# store metadata in a list

for filename in os.listdir("./"):#Each file in currect directory
	if '.xlsx' in filename: 
		#print(filename)
		dt={}
		dt["filename"] = filename 
		status = os.stat(filename) #os.stat contains information like size,last accessed,modified about a file
		dt["access_time"] =datetime.fromtimestamp(status.st_atime).strftime("%m/%d/%y,%H:%M:%S") #store in proper format
		dt["modified_time"]=datetime.fromtimestamp(status.st_mtime).strftime("%m/%d/%y,%H:%M:%S") #store in proper format
		dt["size"] = status.st_size 
		metadata.append(dt)

#print(metadata)
import json
json.dump(metadata,open("metadata.json","w"),indent=4) #Store all metadata in a json file

