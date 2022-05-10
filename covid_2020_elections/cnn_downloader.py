import os
import requests
from helpers import states

races = [ 'PG', 'SG', 'SW' ]

def get_cnn_urls(state):
  # https://politics-elex-results.data.api.cnn.io/results/view/2020-county-races-PG-MI.json
  # https://politics-elex-results.data.api.cnn.io/results/view/2020-district-races-MI.json
  cnn_root_url = 'https://politics-elex-results.data.api.cnn.io/results/view/'
  urls = [
    cnn_root_url+'2020-district-races-'+state+'.json'
  ]

  for race in races:
    urls.append(cnn_root_url+'2020-county-races-'+race+'-'+state+'.json')

  return urls

for state in states:
  urls = get_cnn_urls(state)
  for url in urls:
    data = requests.get(url)
    local_file = covid_data_file = os.path.join(os.path.dirname(__file__), os.pardir, 'data', url.split('/')[-1])
    with open(local_file, 'wb') as file:
      file.write(data.content)