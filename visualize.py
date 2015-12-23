import pandas as pd
import sys
import semantics
import matplotlib.pyplot as plt
import numpy as np
# importing the data #


sample = pd.read_csv('billboard_titles.txt')
sample = sample.set_index('word').to_dict()['count']


default = pd.read_csv('sources/gutenberg10k.txt')
default = default.set_index('word').to_dict()['count']

semantics.plot_freqs(sample)
