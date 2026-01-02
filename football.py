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
    if 'teamsData' in str(el):
        string_with_json_obj = str(el).strip()

#print(string_with_json_obj)

# strip unnecessary symbols and get only JSON data
ind_start = string_with_json_obj.index("('") + 2
ind_end = string_with_json_obj.index("')")
json_data = string_with_json_obj[ind_start:ind_end]

json_data = json_data.encode('utf8').decode('unicode_escape')
json_data = json.loads(json_data)
#save_file = open("player.json", "w")
#json.dump(json_data, save_file, indent = 6)
#save_file.close()

# Get teams and their relevant ids and put them into separate dictionary
teams = {}
for id in json_data.keys():
    teams[id] = json_data[id]['title']

print(teams)

# EDA to get a feeling of how the JSON is structured
# Column names are all the same, so we just use first element
columns = []
for id in json_data.keys():
  columns = list(json_data[id]['history'][0].keys())

# Getting data for all teams
dataframes = {}
for id, team in teams.items():
    teams_data = []
    for row in json_data[id]['history']:
        teams_data.append(list(row.values()))

    df = pd.DataFrame(teams_data, columns=columns)
    dataframes[team] = df
    print('Added data for {}.'.format(team))
print(dataframes)

# Save the dataframe to a CSV file
df.to_csv('teamdata.csv', index=False)
