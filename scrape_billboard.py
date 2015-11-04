from bs4 import BeautifulSoup
import urllib2
import requests
import csv


baseurl = "http://billboardtop100of.com/"

dates = range(1941,2015)

artists = []
songs = []

for date in dates:
    url_end = str(date) + "-2/"
    url = baseurl + url_end
    print url
    temp_artists = []
    temp_songs = []
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    try:
        table = soup.find("table")
        strings = table.find_all('td')
        count = 1
        for i in strings:
            if (count % 3 == 2):
                temp_artists.append(i.string)
            elif (count % 3 == 0):
                temp_songs.append(i.string)
            count = count + 1

    except:
        print "Error: " + str(date)
    artists.append(temp_artists)
    songs.append(temp_songs)
        