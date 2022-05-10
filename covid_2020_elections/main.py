import csv
import json
import os

from helpers import ignored_states, states, clean_fips

covid_data = {}
potus_data = {}
outcome = {}

covid_data_file = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'covid-05-02-2022.csv')

# read covid data
with open(covid_data_file, 'r') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count > 0:
      if row[4] == 'United States' and row[1] != 'NA' and int(row[1]) not in range(80000, 100000):
        covid_data[row[1]] = {
          'fips': row[1],
          'county': row[2],
          'state': row[3],
          'deaths': row[9]
        }
    line_count += 1

# read state potus data
for state in states:
  state_data_file = os.path.join(os.path.dirname(__file__), os.pardir, 'data', f'2020-county-races-PG-{state}.json')
  with open(state_data_file) as json_data:
    state_data = json.loads(json_data.read())
    if state_data is None:
      continue

    for d in state_data:
      county_data = {
        'fips': clean_fips(str(d['countyFipsCode']), d['stateAbbreviation']),
        'county': d['countyName'],
        'state': d['stateAbbreviation'],
      }

      for c in d['candidates']:
        if c['lastName'] in ['Trump', 'Biden']:
          county_data['red' if c['lastName'] == 'Trump' else 'blue'] = c['voteNum']
          county_data['red_percent' if c['lastName'] == 'Trump' else 'blue_percent'] = c['votePercentStr']

      potus_data[county_data['fips']] = county_data

for covid_fips in covid_data:
  cd = covid_data[covid_fips]
  fips = cd['fips']
  deaths = cd['deaths']

  # todo: handle AK (doesn't report votes by county)
  # todo: handle UT (some data missing FIPS?)
  # todo: ignore territories?
  if cd['state'] in ignored_states:
    continue
  
  county_data = potus_data[fips]
  red_deaths = float(deaths) * float(county_data['red_percent'])
  blue_deaths = float(deaths) * float(county_data['blue_percent'])

  new_red = county_data['red'] - red_deaths
  new_blue = county_data['blue'] - blue_deaths

  prev_winner = 'red' if county_data['red'] > county_data['blue'] else 'blue'
  new_winner = 'red' if new_red > new_blue else 'blue'
  flipped = prev_winner != new_winner

  outcome[fips] = {
    'prev_red': county_data['red'],
    'new_red': new_red,
    'prev_blue': county_data['blue'],
    'new_blue': new_blue,
    'prev_winner': prev_winner,
    'new_winner': new_winner,
    'flipped': flipped
  }

# print(outcome['26081'])
print(sum(1 for v in outcome.values() if v['flipped'] is True))
print(len(outcome))