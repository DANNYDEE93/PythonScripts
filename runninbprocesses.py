#import library to show processing systems being utilized
import psutil

#get a list of running processes with column names
import csv
def makeCSV():
  fieldnames = ['pid', 'name', 'exe', 'cpu_percent', 'memory_percent']
  rows = []
#iterate through the list of running processes and append the data to each row
  for proc in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent']):
    rows.append(proc.info)
     

#open CSV file and create object to write into file 
  with open("Running Processes.csv", "w", encoding= "UTF8", newline='') as file:
    writer= csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
#write the prpcesses into each row
    writer.writerows(rows)
print('CSV created')

makeCSV() 
