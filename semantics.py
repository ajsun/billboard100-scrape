# -*- coding: utf-8 -*-
"""
Library of functions to analyze word frequencies and make plots
Created on Wed Dec  9 14:58:27 2015

@author: Rob Whitaker
"""

import matplotlib.pyplot as plt
import numpy as np

# Pleasing colormap to use, 'Tableau 20'
t20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
    (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
    (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
    (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
    (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
# Normalize for the sake of matplotlib
t20 = [(r/255.0, g/255.0, b/255.0) for r,g,b in t20]

def normalize(freqs, count):
    # Normalize a frequency dictionary to occurences per billion
    freqs_normalized = dict()
    for word in freqs:
        freqs_normalized[word] = (freqs[word]/count)*1E7
    return freqs_normalized
    
def compare_freqs(default, sample, n=20, sort='diff', plot_flag=True):
	# compare top word frequencies of a sample to the base language
	# both args should be of type dict with entries {word: p}, p in [0,1]
	if n > len(freqs):
        n = len(sample)

	diffs = dict()
	for word in sample:
	    if word in default:
	        diffs[word] = sample[word] - default[word]
	    else:
	        diffs[word] = sample[word]

    # Do plotting stuff
	if plot_flag:
		# initialize
		plt.figure(figsize=(12,14))
		beautify_plot()

		# sort according to specified argument
		if sort == 'diff':
			words_sorted = sorted(diffs, key=diffs.get, reverse=True)
		elif sort == 'sample':
			words_sorted = sorted(sample, key=sample.get, reverse=True)
		else:
			words_sorted = sorted(default, key=default.get, reverse=True)

		diffs_sorted = [diffs[word] for word in words_sorted]
		sample_sorted = [sample[word] for word in words_sorted]
		default_sorted = [default[word] for word in words_sorted]

		# now plot top n words on alternating horizontal lines 
		plt.ylim(0,2*n)
		# Plot sample frequencies
		plt.barh(range(2*n-1,-1,-2), default_sorted[:n],
			align='center', color=t20[0], alpha=0.8)
		# Plot default frequencies
		plt.barh(range(2*n-2,-1,-2), sample_sorted[:n],
			align='center', color=t20[1], alpha=0.8)

		# Label each bar with its word
		plt.yticks(range(n-1,-1,-1), words_sorted[:n])
		plt.xlabel('Word Frequency (per billlion)')
		#plt.title('Top ' + str(n) + ' words used in Billboard 100 Songs')
		plt.show()

		return diffs
    
def plot_freqs(freqs, n=30):
    # plot top n words and their frequencies from greatest to least
    if n > len(freqs):
        n = len(freqs)
    
    # sort in decreasing order
    words_sorted = sorted(freqs, key=freqs.get, reverse=True)
    freqs_sorted = [freqs[word] for word in words_sorted[:n]]
    
    # plot
    plt.figure(figsize=(12,14))
    beautify_plot()
    plt.ylim(0,n)
    #plt.xlim(0,MAX_OF_FREQS)
    
    # Plot in horizontal bars in descending order
    plt.barh(range(n-1,-1,-1), freqs_sorted, 
             align='center', color=t20[0], alpha=0.8)
    # Label each bar with its word
    plt.yticks(range(n-1,-1,-1), words_sorted)
    plt.xlabel('Word Frequency (per billlion)')
    plt.title('Top ' + str(n) + ' words used in Billboard 100 Songs')
    plt.show()

def beautify_plot():
	# Remove frame and unnecessary tick-marks
	ax = plt.subplot(111)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['left'].set_visible(False)

	# Any other default edits to the plot can go here:


