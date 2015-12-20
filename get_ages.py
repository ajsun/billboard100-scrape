## THIS ONE IS DUMB.  WILL DELETE SOON

from wiki_nav import get_born
import wikipedia
import requests
import pickle

# read in results from billboard scraping
billboard_pkl = open('billboard_data.pkl','rb')
artists = pickle.load(billboard_pkl)
songs = pickle.load(billboard_pkl)
billboard_pkl.close()

# declare start and end years, not sure about architecture here 
# maybe this should all just be in one file?
startYear = 1946
endYear = 2014

# store everything in lists of lists, parallel to artists and songs
birthYears = [];
homeTowns = [];
for date in range(startYear, endYear):
	birthYears.append([])
	homeTowns.append([])
	for artist in artists:
		# search for respective wikipedia pages
		wiki_page = wikipedia.page(artist)
		wiki_url = wiki_page.url
		wiki_html = requests.get(wiki_url)
		info = get_born(wiki_html)

		birthYears[date-startYear].append(info('birthYear'))
		homeTown[date-startYear].append(info('homeTown'))