import pandas as pd
import numpy as np
from tqdm import tqdm

dg = pd.read_csv('genele-genes.csv')


from collections import Counter

### frequency of characters based on the number of times a character appears in the corpus (counts repetition of characters in a single symbol)
def char_frequency(word_list):
    N = len(word_list)
    freq = Counter(''.join(word_list))
    #return {x:v/N for x,v in freq.most_common()}
    return freq

### frequency of characters based on how many symbols contain each character (ignores repetition of characters in a single symbol)
def symbol_frequency(word_list):
    N = len(word_list)
    word_list_distinct = [''.join(set(word)) for word in word_list]
    freq = Counter(''.join(word_list_distinct))
    #return {x:v/N for x,v in freq.most_common()}
    return freq

### based on how often each character appears in a given position 1-5 
def position_frequency(word_list):
    freq = {k:Counter() for k in range(5)}
    for word in word_list:
        for k in range(5):
            freq[k].update(word[k])
    return freq

FREQ_CHAR = char_frequency(dg['symbol'])
FREQ_SYMB = symbol_frequency(dg['symbol'])
FREQ_POS = position_frequency(dg['symbol'])


### functions for calculating frequency score of a give word
def freq_score_sum(word, frequency=FREQ_CHAR):
    return sum(frequency[x] for x in word)

def freq_score_sum_distinct(word, frequency=FREQ_SYMB):
    return sum(frequency[x] for x in set(word))

def freq_score_sum_pos(word, frequency=FREQ_POS):
    return sum(frequency[k][x] for k,x in enumerate(word))