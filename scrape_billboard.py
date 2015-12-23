from bs4 import BeautifulSoup
import requests
#initialize
billboard = Billboard()

# range
startYear = 1946
endYear = 2015
dates = range(startYear,endYear)

# main loop
baseurl = "http://www.bobborst.com/popculture" + \
    "/top-100-songs-of-the-year/?year="
    
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
        billboard.add_entry(entry)

num_words, word_freqs = billboard.word_count(False)

del(startYear,endYear,dates,baseurl,url,date,
    rows,cell,cells,html,soup,table)