class CovidData:
  def __init__(self, state, county, fips, deaths) -> None:
      self.state = state
      self.county = county
      self.fips = fips
      self.deaths = deaths