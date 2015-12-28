# classes for billboard scraping
import re, wikipedia, requests
from bs4 import BeautifulSoup

# container for all billboard entries
class Billboard:
    # construct with blank list of entries
    def __init__(self, start_year=1946, entries_per_year=100):
        self.entries = []
        self.start_year = start_year
        self.entries_per_year = entries_per_year

    def __str__(self):
        to_string = ''
        for entry in self.entries:
            to_string += str(entry)
        return to_string

    def __len__(self):
        return len(self.entries)

    # add entry
    def add_entry(self, new_entry):
        self.entries.append(new_entry)

    def word_count(self, print_flag=False):
        # initialize dictionary of {word: frequency}
        freqs = dict()
        num_words = 0

        # Generate regular expressions to clean titles
        excluded_chars = re.compile("[][,!@#$%^&*()+:;?'\"-]")
        space_chars = re.compile('[./-]')

        # loop through each title
        for entry in self.entries:
            # Clean up title
            clean_title = excluded_chars.sub('', entry.title)
            clean_title = space_chars.sub(' ', clean_title)

            # loop through each word in the title
            for word in clean_title.split():
                # keep total count
                num_words += 1
                
                # update dictionary, case insensitive
                word = word.lower()
                if word in freqs:
                    freqs[word] += 1
                else:
                    freqs[word] = 1

        # print in order
        if print_flag:
            # sort by most frequent to output
            for word in sorted(freqs, key=freqs.get, reverse=True):
                print(word, freqs[word])

        return num_words, freqs

    def search(self, query):
        # Return a sub-billboard with only entries that match a query

        # TODO 

        return None

    def grab(self, year, position):
        # Return a specific entry from year and position
        if year < self.start_year:
            return None

        # Calculate location in list
        years_in = year - self.start_year
        entry_num = years_in * self.entries_per_year + position

        return self.entries[entry_num]

class Entry:
    # construct with basic info
    def __init__(self, date, info):
        # year of billboard entry
        self.date = date
        # info is the triplet [pos, artist, title]
        self.pos = info[0]
        self.artist = info[1]
        self.title = info[2]

        # trim the artist name
        feat = self.artist.find('feat')
        if feat >= 0:
            self.artist = self.artist[:feat]

        # has entry been completed?
        self.completed = False

    def __len__(self):
        return len(self.members)

    def complete(self):
        # invoke further scraping methods to complete entry
        self.set_members()
        self.birth_years, self.birth_places = self.get_born()
        self.completed = True

    def set_members(self):
        # TODO: handle the case with collaboration between artists

        # find artist's wikipedia page
        try:
            wiki_page = wikipedia.page(self.artist)
        except:
            print('Artist wikipedia page not found')
            raise

        # Parse wikipedia page
        wiki_html = requests.get(wiki_page.url).text
        soup = BeautifulSoup(wiki_html, 'lxml')

        # Infobox is wikipedia sidebar with basic info
        infobox = soup.find(class_ = 'infobox')
        if infobox == None:
            print('Wikipedia page missing infobox')
            raise

        # Look for entry in infobox listing members
        membersRow = infobox.find('th', text=['Members', 'Past members'])
        if membersRow == None:
            self.members = [self.artist]
            return

        # If the row exists, go to the list of members and add to list
        self.members = []
        membersBox = membersRow.find_next_sibling('td')
        for member in membersBox.stripped_strings:
            self.members.append(member)

    def get_born(self):
        if not self.members:
            raise

        birth_years = []
        birth_places = []
        for person in self.members:
            # Find band member wikipedia page
            try:
                wiki_page = wikipedia.page(person)
            except:
                birth_places.append('Not Found')
                birth_years.append('Not Found')
                continue

            # Parse wikipedia page
            wiki_html = requests.get(wiki_page.url).text
            soup = BeautifulSoup(wiki_html, 'lxml')
            infobox = soup.find(class_ = 'infobox')
            if infobox == None:
                birth_places.append('Not Found')
                birth_years.append('Not Found')
                continue

            # Get birthplace
            birth_place_node = infobox.find('span', class_ = 'birthplace')
            birth_place = str()
            if birth_place_node != None:
                for s in birth_place_node.strings:
                    birth_place += s
            else:
                birth_place = 'Not Found'

            birth_places.append(birth_place)

            # get birth year
            bday_node = infobox.find('span', class_ = 'bday')
            if bday_node != None:
                birth_year = int(bday_node.string[0:4])
            else:
                birth_year = 'Not Found'

            birth_years.append(birth_year)

        return [birth_years, birth_places]

    def get_lyrics(self):
        # Pull lyrics off of genius.com, TODO: use other sites as backup
        baseurl = 'http://genius.com/'
        # convert song title to page ID in style of genius.com
        artist = re.sub('\s', '-', self.artist)
        title = re.sub('\s', '-', self.title)
        lyrics_url = baseurl + artist + '-' + title + '-lyrics'
        # parse lyrics page via soup
        lyrics_html = requests.get(lyrics_url).text
        lyrics_soup = BeautifulSoup(lyrics_html)
        # search for lyrics on page / confirm the page exists
        lyrics = ''
        lyrics_container = lyrics_soup.find('div', class_='lyrics_container')
        if lyrics_container == None:
            return '*Lyrics not found'
        for line in lyrics_container.find('p').stripped_strings:
            lyrics += line + '\n'

        # trim lyrics for bracket sections / attributions
        lyrics = re.sub('\[.*\]', '', lyrics)
        return lyrics

    def get_age(self):
        # determine age of performer(s) in billboard year
        ages = []
        for year in self.birth_years:
            if isinstance(year,int):
                ages.append(self.date - year)
            else:
                ages.append('Uknown')

        return ages

    # Ways of print_flag 
    def __str__(self):
        to_string = '\n' + str(self.date) + ' - Position:' + str(self.pos) + \
            '\n "' + self.title + '" by ' + self.artist + '\n'
        return to_string

    def detail(self):
        if self.completed:
            to_string = str(self)
            for person, place, year, age in zip(self.members, 
                self.birth_places, self.birth_years, self.get_age()):
                to_string += '\n' + person + '\n\tHometown: ' + \
                    place + '\n\tBirthyear: ' + str(year) + \
                    '\n\tAge at release: ' + str(age)
            return to_string
        else:
            to_string = str(self) + '\n' + \
                'Homewtown(s): ' + 'Unset' + '\n' + \
                'Birthyear(s): ' + 'Unset' + '\n'
            return to_string

# basic client
if __name__ == '__main__':
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