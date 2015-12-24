import pandas as pd
import sys
import semantics
import matplotlib.pyplot as plt
import numpy as np
# importing the data #



sample = semantics.return_dict('billboard_titles.txt')
default = semantics.return_dict('sources/gutenberg10k.txt')

semantics.plot_freqs(sample)
semantics.plot_freqs(default)

semantics.compare_freqs(default, sample)