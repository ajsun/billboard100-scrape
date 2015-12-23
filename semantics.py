# -*- coding: utf-8 -*-
"""
Library of functions to analyze word frequencies and make plots
Created on Wed Dec  9 14:58:27 2015

@author: Rob Whitaker
"""

import matplotlib.pyplot as plt
import numpy as np
import re

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
        freqs_normalized[word] = (freqs[word]/count)*1E9
    return freqs_normalized
    
def compare_freqs(default, sample, default_label='Default',
		sample_label='Sample', n=20, sort='diff', plot_flag=True):
	# compare top word frequencies of a sample to the base language
	# both args should be of type dict with entries {word: p}, p in [0,1]
	if n > len(sample):
		n = len(sample)

	diffs = dict()
	for word in sample:
	    if word in default:
	        diffs[word] = sample[word] - default[word]
	    else:
	    	# 
	        diffs[word] = sample[word]
	        # Add to default dictionary 
	        default[word] = 0

    # Do plotting stuff
	if plot_flag:
		# initialize
		fig = plt.figure(figsize=(6,4))
		beautify_plot(fig)

		# sort according to specified argument
		if sort == 'diff':
			words_sorted = sorted(diffs, key=diffs.get, reverse=True)
		elif sort == 'sample':
			words_sorted = sorted(sample, key=sample.get, reverse=True)
		else:
			words_sorted = sorted(default, key=default.get, reverse=True)

		# sort each list of values
		diffs_sorted = [diffs[word] for word in words_sorted[:n]]
		sample_sorted = [sample[word] for word in words_sorted[:n]]
		default_sorted = [default[word] for word in words_sorted[:n]]

		# Set locations for bars and labels
		bar_width = 0.4
		sample_locs = np.arange(n, 0, -1) + bar_width/2
		default_locs = np.arange(n, 0, -1) - bar_width/2
		label_locs = np.arange(n, 0, -1)

		# Plot sample frequencies
		sample_bars = plt.barh(sample_locs, sample_sorted,
			align='center', color=t20[2], alpha=0.8, label=sample_label,
			height=bar_width, linewidth=0)
		# Plot default frequencies
		default_bars = plt.barh(default_locs, default_sorted,
			align='center', color=t20[1], alpha=0.8, label=default_label,
			height=bar_width, linewidth=0)

		# Label each pair of bars with its word
		plt.title('Frequencies of popular words (per billlion)')
		plt.yticks(label_locs, words_sorted)
		plt.ylim(0,n+1)

		# Legend
		leg = plt.legend(handles=[sample_bars,default_bars], loc=4)
		leg.draw_frame(False)

		# Finally, show the plot
		plt.show()

	return diffs


def beautify_plot(fig):
	# Set background color to white
	fig.patch.set_facecolor((1,1,1))

	# Remove frame and unnecessary tick-marks
	ax = plt.subplot(111)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['left'].set_visible(False)

	plt.tick_params(axis='y', which='both', left='off', right='off')
	plt.tick_params(axis='x', which='both', top='off', bottom='off')

	# Any other default edits to the plot can go here:
	# figure doesn't need to be returned as the pass was by reference


def plot_freqs(freqs, n=30):
    # plot top n words and their frequencies from greatest to least
    if n > len(freqs):
        n = len(freqs)
    
    # sort in decreasing order
    words_sorted = sorted(freqs, key=freqs.get, reverse=True)
    freqs_sorted = [freqs[word] for word in words_sorted[:n]]
    
    # plot
    fig = plt.figure(figsize=(6,4))
    beautify_plot(fig)
    plt.ylim(0,n)
    #plt.xlim(0,MAX_OF_FREQS)
    
    # Plot in horizontal bars in descending order
    bar_locs = np.arange(n, 0, -1)
    bar_width = 1.0
    plt.barh(bar_locs, freqs_sorted, height=bar_width,
             align='center', color=t20[0], alpha=0.8, linewidth=0)

    # Label each bar with its word
    plt.yticks(range(n-1,-1,-1), words_sorted)
    plt.xlabel('Word Frequency (per billlion)')
    plt.title('Top ' + str(n) + ' words used in Billboard 100 Songs')
    plt.show()

def read_freqs(text_file):
	# read a three-column text file of rank / word / frequency
	# open file
	fhandle = open(text_file, 'r')
	full_text = fhandle.read()
	# initialize dictionary
	freqs = dict()

	#Compile excluded characters 
	excluded_chars = re.compile("[][,!@#$%^&*()+:;?'\"-]")

	# loop through each line
	for line in full_text.split('\n'):
		split_line = line.split()
		if len(split_line) == 3:
			# Clean up contractions etc.
			word = excluded_chars.sub('', split_line[1])
			# Convert frequency to double
			freq = float(split_line[2])
			# add to dictionary
			freqs[word] = freq

	return freqs

def write_freqs(filename, freqs):
	fhandle = open(filename, 'w')
	# Sort and write to file in sorted order
	words_sorted = sorted(freqs, key=freqs.get, reverse=True)
	freqs_sorted = [freqs[word] for word in words_sorted]

	for i in range(len(words_sorted)):
		fhandle.write(str(i) + '\t')
		fhandle.write(str(words_sorted[i]) + '\t')
		fhandle.write(str(freqs_sorted[i]) + '\n')

	fhandle.close()
