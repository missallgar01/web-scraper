import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
import lxml
import json
from bs4 import BeautifulSoup

base_url = 'https://understat.com/league'
leagues = ['EPL']
seasons = ['2023']

url = base_url+'/'+leagues[0]+'/'+seasons[0]
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")

# Based on the structure of the webpage, I found that data is in the JSON variable, under 'script' tags
scripts = soup.find_all('script')

string_with_json_obj = ''

# Find data for teams
for el in scripts:
    if 'playersData' in str(el):
        string_with_json_obj = str(el).strip()

#print(string_with_json_obj)

# strip unnecessary symbols and get only JSON data
ind_start = string_with_json_obj.index("('") + 2
ind_end = string_with_json_obj.index("')")
json_data = string_with_json_obj[ind_start:ind_end]

json_data = json_data.encode('utf8').decode('unicode_escape')
json_data = json.loads(json_data)

#print(json_data)
#save_file = open("player.json", "w")
#json.dump(json_data, save_file, indent = 6)
#save_file.close()

# Get players and their relevant ids and put them into separate dictionary
players = {}
for player in json_data:
    #print(player)
    players['id'] = player['id']
    players['name'] = player['player_name']
    #print(players)


# Column names are all the same, so we just use first element
columns = []
for player in json_data:
  columns = list(player.keys())

print(columns)

# Getting data for all teams


players_data = []
for player in json_data:
    players_data.append(list(player.values()))
    #print(players_data)
    print('Added data for {}.'.format(player['player_name']))
#print(players_data)
df = pd.DataFrame(players_data, columns=columns)
print(df)

# Save the dataframe to a CSV file
df.to_csv('players.csv', index=False)

