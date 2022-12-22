import requests
from bs4 import BeautifulSoup

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
