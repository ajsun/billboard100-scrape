# classes for billboard scraping
import re

# container for all billboard entries
class Billboard:
    # construct with blank list of entries
    def __init__(self):
        self.entries = [];

    # use list iterator
    # def __iter__(self):
    #     return self

    def __str__(self):
        to_string = ''
        for entry in self.entries:
            to_string += str(entry)
        return to_string

    # add entry
    def add_entry(self, new_entry):
        self.entries.append(new_entry)

    def word_count(self, print_flag=True):
        # initialize dictionary of {word: frequency}
        freqs = dict()
        num_words = 0

        # Generate regular expressions to clean titles
        excluded_chars = re.compile("[],!@#$%^&*()+:;?'\"-]")
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

class Entry:
    # construct with basic info
    def __init__(self, date, info):
        # year of billboard entry
        self.date = date
        # info is the triplet [pos, artist, title]
        self.pos = info[0]
        self.artist = info[1]
        self.title = info[2]
        # has entry been completed?
        self.completed = False

    # Methods to act on the object
    def complete(self):
        # invoke further scraping methods to complete entry
        self.members = get_members(self.artist)
        self.birthYear, self.homeTown = get_born(self.members)
        self.completed = True

    # Methods to perform calculations etc. on object
    def get_age(self):
        # determine age of performer(s) in billboard year
        if len(self.birthYear) == 1:
            return [self.date - self.birthYear[0]]
        else:
            ages = []
            for year in self.birthYear:
                ages.append(self.date - year)
            return ages

    def get_size(self):
        return len(self.members)

    # Ways of print_flag 
    def __str__(self):
        to_string = '\n' + str(self.date) + ' - Position:' + str(self.pos) + \
            '\n "' + self.title + '" by ' + self.artist + '\n'
        return to_string

    def detail(self):
        if self.completed:
            to_string = str(self) + '\n' + \
                'Homewtown(s):' + self.homeTown + '\n' + \
                'Birthyear(s):' + self.birthYear + '\n'
            return to_string
        else:
            to_string = str(self) + '\n' + \
                'Homewtown(s):' + 'Unset' + '\n' + \
                'Birthyear(s):' + 'Unset' + '\n'
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