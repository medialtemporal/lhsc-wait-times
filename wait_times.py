import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timezone, timedelta


lhsc_site = requests.get('https://www.lhsc.on.ca/adult-ed/emergency-department-wait-times')

soup = BeautifulSoup(lhsc_site.text, 'html.parser')

# Finding wait time values
wait_times = []
h1 = soup.find_all('h1')

for item in h1:
    if not item.find('span'):  # gets rid of an extraneous h1 tag
        wait_times.append(item.contents[:2])


# Finding last update times
last_update = []
p = soup.find_all('p')

for item in p:
    if item.find('span'):
        if len(item.find('span').contents) > 1:  # gets rid of extraneous tags
            last_update.append(item.find('span').contents[:2])


# Print statements (test)
print(f'London ER Wait Times\n'
      f'University Hospital: {wait_times[0][1]} (last update: {last_update[0][1]})\n'
      f'Victoria Hospital: {wait_times[1][1]} (last update: {last_update[1][1]})')


# Clean up numbers for writing to csv

timezone_offset = -5.0  # Eastern Standard Time (UTC-5:00)
tzinfo = timezone(timedelta(hours=timezone_offset))
today = datetime.now(tzinfo)
today = today.strftime("%Y-%m-%d")

in_time = datetime.strptime(last_update[0][1], "%I:%M %p")  # changing time from 12h to 24h
out_time = datetime.strftime(in_time, "%H:%M")


uh_string = ""
for character in wait_times[0][1]:  # University Hospital
    if character.isnumeric() or character == '.':
        uh_string = uh_string + character


vh_string = ""
for character in wait_times[1][1]:  # Victoria Hospital
    if character.isnumeric() or character == '.':
        vh_string = vh_string + character


# Writing update to csv file
with open('data.csv', 'a') as file:
    writer = csv.writer(file)
    writer.writerow([today,out_time,uh_string,vh_string])
