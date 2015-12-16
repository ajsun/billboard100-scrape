from bs4 import BeautifulSoup
import requests, wikipedia, csv
# import sys

def get_born(artist):
    notFound = {'birthPlace':'Not Found', 'birthYear':'Not Found'}

    # Retrieve the birth place and birthdate information of an artist
    try:
        wiki_page = wikipedia.page(artist + ' (band)')
    except:
        return notFound

    wiki_html = requests.get(wiki_page.url).text
    soup = BeautifulSoup(wiki_html, 'lxml')

    infobox = soup.find(class_ = 'infobox')
    if infobox == None:
        return notFound

    # Test whether or not it's a band or single person
    if infobox.find('th', text = ['Members', 'Past members']) == None:
        return get_born_person(infobox)
    else:
        info = {'birthPlace':[],'birthYear':[]}

        # Find all band members
        membersRow = infobox.find('th', text = ['Members', 'Past members'])
        membersBox = membersRow.find_next_sibling('td')

        # Get each member's respective wikipedia page and born info
        if membersBox.find('a') != None:
            for a in membersBox.find_all('a'):
                member_html = requests.get('http://wikipedia.com' + a['href'])
                member_soup = BeautifulSoup(member_html.text, 'lxml')
                member_infobox = member_soup.find(class_ = 'infobox')
                if member_infobox != None:
                    member_info = get_born_person(member_infobox)

                    # concatenate born info into a single dict
                    info['birthPlace'].append(member_info['birthPlace'])
                    info['birthYear'].append(member_info['birthYear'])
            return info
        else:
            return notFound

def get_born_person(infobox):    
    # Return the birth place and birthdate of a single person

    # get birthplace
    birthPlace_node = infobox.find('span', class_ = 'birthplace')
    birthPlace = str()
    if birthPlace_node != None:
        for s in birthPlace_node.strings:
            birthPlace += s
    else:
        birthPlace = 'Not Found'

    # get birth year
    bday_node = infobox.find('span', class_ = 'bday')
    if bday_node != None:
        birthYear = int(bday_node.string[0:4])
    else:
        birthYear = 'Not Found'

    return {'birthPlace':birthPlace, 'birthYear':birthYear}


#host for billboard top 100
baseurl = "http://www.bobborst.com/popculture/top-100-songs-of-the-year/?year="

startYear = 1946
endYear = 2015
dates = range(startYear,endYear)

#initialize parallel lists to hold data:
#each is a list of top 100 lists by year
artists = []
songs = []
birthYears = []
homeTowns = []

print('Scraping billboard:')
for date in dates:
    print(str(date) + '...', end = '')
    #get soup
    url = baseurl + str(date)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    table = soup.find("tbody")
    cells = table.find_all('td')
    
    #pull stuff from soup
    artists.append([])
    songs.append([])
    birthYears.append([])
    homeTowns.append([])
    count = 1
    for cell in cells:
        #first cell in each row is rank, second artist, third song
        if (count % 3 == 2):
            artist = cell.string
            artists[date-startYear].append(artist)

            #get birthdate and birthPlace from respective wikipedia page
            info = get_born(artist)

            birthYears[date-startYear].append(info['birthYear'])
            homeTowns[date-startYear].append(info['birthPlace'])

        elif (count % 3 == 0):
            songs[date-startYear].append(cell.string)
            # do stuff for lexical analysis here?
    
        count += 1
    print('Done!')

# output results to csv: 


# #Alternatively, save the data using pickle
# pkl_file = open('billboard_data.pkl','wb')
# #increase max recursion depth or this crashes
# sys.setrecursionlimit(10000)
# #dump
# pickle.dump(artists, pkl_file)
# pickle.dump(songs, pkl_file)
# pkl_file.close()