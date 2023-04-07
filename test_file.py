import requests
from selectorlib import Extractor

class Temperature:
    """
        timeanddate.com/weather
    """
    yaml_string = """
        temp:
            xpath: '/html/body/div[5]/main/article/section[1]/div[1]/div[2]'

    """
    base_url ='https://www.timeanddate.com/weather/'

    def __init__(self, country, city):
        self.country = country.replace(' ', '-')
        self.city = city.replace(' ', '-')

    def _build_url(self):
        url = self.base_url + self.country + '/' + self.city
        return url
    
    def _scrape(self):
        # url
        url = self._build_url()
        extractor = Extractor.from_yaml_string(self.yaml_string) 
        req = requests.get(url, headers=self.headers)
        full_content = req.text
        raw_content = extractor.extract(full_content)
        # ['temp']
        return raw_content

    def get(self):
        scraped_content = self._scrape()
        return float(scraped_content['temp'].replace('°C', '').strip())

if __name__ == '__main__':
    temp = Temperature(country='usa', city='san francisco')
    print(temp.get())
rr = 'AKIATSB4DW2EQFDMJEMV'