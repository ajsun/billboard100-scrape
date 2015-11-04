from bs4 import BeautifulSoup
import requests
import csv


baseurl = "http://www.bobborst.com/popculture/top-100-songs-of-the-year/?year="

startYear = 1941
endYear = 2015
dates = range(startYear,endYear)

artists = []
songs = []
for date in dates:
    #get soup
    url = baseurl + str(date)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    table = soup.find("tbody")
    cells = table.find_all('td')
    
    #pull stuff from soup
    artists.append([])
    songs.append([])
    count = 1
    for cell in cells:
        if (count % 3 == 2):
            artists[date-startYear].append(cell.string)
        elif (count % 3 == 0):
            songs[date-startYear].append(cell.string)
        count += 1

print(artists)
print(songs)