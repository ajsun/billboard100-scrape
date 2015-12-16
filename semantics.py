# -*- coding: utf-8 -*-
"""
analyze word frequencies
Created on Wed Dec  9 14:58:27 2015

@author: Rob Whitaker
"""

import matplotlib.pyplot as plt
from tableau import t20_norm as t20
import numpy as np

def normalize(freqs, count):
    # Normalize a frequency dictionary to fractions
    freqs_normalized = dict()
    for word in freqs:
        freqs_normalized[word] = freqs[word]/count
    return freqs_normalized
    
def compare_freqs(default, sample):
    # compare top word frequencies of a sample to the base language
    # both args should be of type dict with entries {word: p}, p in [0,1]
    diffs = dict()
    for word in sample:
        if word in default:
            diffs[word] = sample[word] - default[word]
        else:
            diffs[word] = sample[word]

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
    ax = plt.subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.ylim(0,n)
    #plt.xlim(0,MAX_OF_FREQS)
    
    
    plt.barh(range(n-1,-1,-1), freqs_sorted, 
             align='center', color=t20[0], alpha=0.8)
    plt.yticks(range(n-1,-1,-1), words_sorted)
    plt.xlabel('Word Frequency')
    plt.title('Top ' + str(n) + ' words used in Billboard 100 Songs')
    plt.show()
