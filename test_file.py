import requests
from selectorlib import Extractor

class Temperature:
    """
        timeanddate.com/weather
    """
    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
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

"""
headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
"""

if __name__ == '__main__':
    temp = Temperature(country='usa', city='san francisco')
    print(temp.get())

SECRET_KEY = 'django-insecure-^k^8ce44l(&^%gbh$361$xgp@dixlh#!%7279^vuk9*v454-s6'
aws_secret = "AKIATSB4ZW2XQFLMJYUI"
