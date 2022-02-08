from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError

targetDomain = input("Enter domain name EXACTLY with http://www.")
try:
    html = urlopen(targetDomain)
except HTTPError as e:
    print(e)
except URLError as e:
    print('The server couldn\'t be found! Invalid url?')
else:
    #Code continues
    bs = BeautifulSoup(html.read(), 'html.parser')
    print(bs)
