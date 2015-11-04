from bs4 import BeautifulSoup
import urllib2
import re
import csv


baseurl = "http://billboardtop100of.com/"

dates = range(1941,2015)

for date in dates:
    url_end = str(date) + "-2/"
    url = baseurl + url_end
    print url
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    try:
        table = soup.find(class_="alignleft")
        strings = table.find_all('td')
        for i in strings:
            print i.string
    except:
        print "Error: " + str(date)
        
