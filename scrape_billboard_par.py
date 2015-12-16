from bs4 import BeautifulSoup
from wiki_nav import get_born
from threading import Thread
from queue import Queue
from billboard import Billboard, Entry
import requests, wikipedia, csv

def scrape(entry_queue, billboard):
    #Each worker will keep grabbing entries until the queue is empty
    while True:
        #pop an entry from the queue
        entry = entry_queue.get()
        if entry != None:
            #get birthdate and birthPlace from respective wikipedia page
            entry.complete()
            billboard.add_entry(entry)
            #print(entry)
        # tell the queue we finished
        entry_queue.task_done()

#host for billboard top 100
baseurl = "http://www.bobborst.com/popculture/top-100-songs-of-the-year/?year="

# initialize queue to hold each cell and Billboard for results
entry_queue = Queue()
billboard = Billboard()

# open threads 
max_workers = 200
for i in range(max_workers):
    worker = Thread(target = scrape, args = (entry_queue, billboard))
    worker.daemon = True
    worker.start()

# parameters of search
startYear = 1946
endYear = 2015
dates = range(startYear,endYear)

# main loop
print('Scraping billboard:')
for date in dates:
    # output progress
    print(str(date) + '...')

    # get soup
    url = baseurl + str(date)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    table = soup.find('tbody')
    rows = table.find_all('tr')
    
    # queue each cell for further scraping
    for row in rows:
        # create list: [position, artist, title]
        cells = []
        for cell in row.children:
            if cell.string != '\n':
                cells.append(cell.string)

        # create entry object 
        entry = Entry(date, cells)
        entry_queue.put(entry)

# force the queue to empty
entry_queue.join()

# print results
print(billboard)
# output results to csv: 
# TODO 
