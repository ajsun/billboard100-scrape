import requests
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue

# (play around with threading etc.)
# Goal: open a wikipedia page, get all links, print the title of every page linked to

# function to follow link and print title
def follow_link(url_queue, id):
	# link following function for a worker to perform until empty
	while True:
		# pop a new url from the queue
		# print('Worker #', id, 'waiting')
		url = url_queue.get()
		if url != None:
			# follow link
			if url.find('/wiki/') == 0:
				# print('Worker #', i, url)
				# internal (wikipedia) link
				url = 'http://www.wikipedia.org' + url
				html = requests.get(url).text
				soup = BeautifulSoup(html)
				title = soup.find('title')
				print(title.string)

		# tell worker we did it
		url_queue.task_done()

# first open threads and create queue
max_workers = 200
url_queue = Queue()

for i in range(max_workers):
	worker = Thread(target = follow_link, args = (url_queue, i))
	worker.setDaemon = True
	worker.start()

#begin task
source = 'http://www.wikipedia.org/wiki/Python_(programming_language)'
source_html = requests.get(source).text
source_soup = BeautifulSoup(source_html)
anchors = source_soup.find_all('a')

# populate queue with all links to visit
for tag in anchors:
	# print('Queuing', tag.get('href'))
	url_queue.put(tag.get('href'))

# wait for everyone to finish
url_queue.join()
