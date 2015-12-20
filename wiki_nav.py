from bs4 import BeautifulSoup
import requests, wikipedia
# collection of methods designed to navigate and extract info from wikipedia

def get_born(artist):
    notFound = ['Not Found', 'Not Found']

    # Retrieve the birth place and birthdate information of an artist
    try:
        wiki_page = wikipedia.page(artist)
    except:
        try:
            wiki_page = wikipedia.page(artist + ' (band)')
        except:
            return notFound
            
    # TODO:
    # Still need to handle the case of collabs, aka artist = artist1, artist2
    # Also these multiple try-catch blocks seem inelegant, fix it

    wiki_html = requests.get(wiki_page.url).text
    soup = BeautifulSoup(wiki_html, 'lxml')

    infobox = soup.find(class_ = 'infobox')
    if infobox == None:
        return notFound

    # Test whether or not it's a band or single person
    if infobox.find('th', text = ['Members', 'Past members']) == None:
        return get_born_person(infobox)
    else:
        info = [[],[]]

        # Find all band members
        membersRow = infobox.find('th', text = ['Members', 'Past members'])
        membersBox = membersRow.find_next_sibling('td')

        # Get each member's respective wikipedia page and born info
        if membersBox.find('a') != None:
            for a in membersBox.find_all('a'):
                try:
                    member_html = requests.get(
                        'http://wikipedia.com' + a['href'])
                except:
                    return notFound
                member_soup = BeautifulSoup(member_html.text, 'lxml')
                member_infobox = member_soup.find(class_ = 'infobox')
                if member_infobox != None:
                    member_info = get_born_person(member_infobox)

                    # concatenate born info into a single dict
                    info[0].append(member_info[0])
                    info[1].append(member_info[1])
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

    return [birthPlace, birthYear]

    