states = [ 'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY' ]
ignored_states = ['Alaska', 'Utah', 'American Samoa', 'Guam', 'Northern Mariana Islands', 'Puerto Rico', 'Virgin Islands']

def clean_fips(fips, state):
  # CNN data shows CT FIPS as '90900001' instead of '09001'
  if state in ['Connecticut', 'CT']:
    return f'09{fips[-3:]}'

  # DC cuz CNN uses '1' instead of '11001'
  if state in ['District of Columbia', 'DC']:
    return '11001'

  # ME cuz CNN uses '92300001' instead of '23001'
  if state in ['Maine', 'ME']:
    # handle this especially stupid case for Waldo County
    # CNN has '92300466' but it's '23027'
    if fips == '92300466':
      return '23027'

    return f'23{fips[-3:]}'

  if state in ['Massachusetts', 'MA']:
    return f'25{fips[-3:]}'

  if state in ['New Hampshire', 'NH']:
    return f'33{fips[-3:]}'

  if state in ['Rhode Island', 'RI']:
    return f'44{fips[-3:]}'

  if state in ['Vermont', 'VT']:
    return f'50{fips[-3:]}'

  return fips