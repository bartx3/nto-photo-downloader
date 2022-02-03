#!/usr/bin/python3
#
#Author: Bartłomiej Sitnik
#My github: https://github.com/bartx3
#Repository: https://github.com/bartx3/nto-photo-downloader
#License (MIT): https://github.com/bartx3/nto-photo-downloader/blob/main/LICENSE
#

import requests
from urllib.parse import urlparse
import _thread

def download (source, filename):
    data = requests.get(source)
    with open((str(filename) + source[source.rfind("."):]), 'wb') as file:
        file.write(data.content)

url = input("Podaj url do pierwszego zdjęcia:\n")
resp = requests.get(url)
licznik = 0
foundurl = 1
path = urlparse(url).path
path = path[1:(path[1:].find('/')+1)]
while (foundurl!=-1 and resp.status_code == 200):
    licznik += 1
    print("Udało się dostać do ", licznik, " strony pod adresem ", resp.url, '\n')
    cont = str(resp.content)
    pos = cont.rfind('as="image"')
    posurlph = cont.find('https:', pos)
    posurlph2 = cont.find('"', posurlph)
    urlph = cont[posurlph:posurlph2]
    if (urlph != ""):
        print ("Znaleziono obraz: ", urlph, '\n')
        _thread.start_new_thread( download, (urlph, licznik))
    else:
        print ("Na stronie nr ", licznik, " nie znaleziono zdjęcia :(")
    #Looking for the next url
    pos = cont.find('"nextPageUrl"')
    posurl = cont.find(path, pos)
    foundurl = min(pos, posurl, foundurl)
    if (foundurl!=-1):
        posurl2 = cont.find('"', posurl)
        url1 = cont[posurl:posurl2]
        url1 = urlparse(url).scheme + "://" + urlparse(url).netloc + "/" + url1.replace("\\", "")
        print ("Znaleziono adres kolejnej strony: " + url1 + '\n')
        resp = requests.get(url1)
        if(resp.status_code != 200):
            print("Nie można otworzyć kolejnej strony! \n", "Status code: ", resp.status_code, "\n") 
    else:
        print("Nie udało się dostać do kolejnego url\n")
