import json
import csv
import requests

url = "https://free-nba.p.rapidapi.com/players"

#set headers and params
headers = {
  "X-RapidAPI-Key": "your-api-key",
  "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
}
params = {
  "page":"1",
  "per_page":"100"
}

#define variables
response = requests.get(url, headers=headers, params=params)
responses = response.json()
players = responses["data"]
print(responses)

#Handle the potential HTTPError for API authentication 
try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
except requests.HTTPError as e:
  print(e)
  exit()

# Check for errors in response  
if "error" in response.json():
  print(response.json()["error"])
  exit()

# Get data if no errors
data = response.json()['data']


#Create function to create a csv file with NBA data from API
def makeCSV():
  fieldnames = ['id', 'first_name', 'last_name', 'position','name' ]
  rows =[]

#iterate through player data and append the listed data to rows within the csv file    
  for player in players(0, players):
    rows.append({'id':responses['data'][player]['id'], 
    'first_name':responses['data'][player]['first_name'], 
    'last_name':responses['data'][player]['last_name'],
    'position':responses['data'][player]['position'],
    'name':responses['data'][player]["team"]["name"]
})

#open CSV file and create object to write into file as a dictionary 
  with open("nbaPlayers.csv", "w", encoding = "UTF8", newline='') as file:
#write into the file with parameters for the columns, header, and rows 
    writer= csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print('CSV Created')

makeCSV()
