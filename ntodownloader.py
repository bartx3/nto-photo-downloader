import requests
from urllib.parse import urlparse

url = input("Podaj url do pierwszego zdjęcia:\n")
resp = requests.get(url)
licznik = 0
foundurl = 1
path = urlparse(url).path
path = path[1:path.find('/')]
while (foundurl!=-1 and resp.status_code == 200):
    licznik += 1
    print("Udało się dostać do ", licznik, " strony pod adresem ", url, '\n')
    cont = str(resp.content)
    pos = cont.rfind('as="image"')
    posurlph = cont.find('https:', pos)
    posurlph2 = cont.find('"', posurlph)
    urlph = cont[posurlph:posurlph2]
    print ("Znaleziono obraz: ", urlph, '\n')
    #Szukanie rozszerzenia i ustalanie nazwy pliku
    extention = urlph[urlph.rfind("."):]
    fname = str(licznik) + "." + extention
    data = requests.get(urlph)
    with open(fname, 'wb') as file:
        file.write(data.content)
    #Szukanie linku do kolejnego zdjęcia
    pos = cont.find('"nextPageUrl"')
    posurl = cont.find(path, pos, pos+100)
    foundurl = min(pos, posurl, foundurl)
    if (foundurl!=-1):
        posurl2 = cont.find('"', posurl)
        url1 = cont[posurl:posurl2]
        url1 = urlparse(url).netloc + url1.replace("\\", "")
        resp = requests.get(url)
    else:
        print("Nie udało się dostać do kolejnego url\n")
