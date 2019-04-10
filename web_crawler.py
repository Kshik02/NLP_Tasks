import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#Parsing all the links from youtube
url = 'https://www.youtube.com/'
content = requests.get(url)
soup = BeautifulSoup(content.text, 'html.parser')

try:
    for elem in soup.find_all("a", href=True):
        print(elem.string)
        print(urljoin(url, elem['href']))
except:
    print('Error!')
