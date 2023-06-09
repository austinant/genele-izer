### build genele updating word list class
import pandas as pd
from frequency import *
from collections import Counter

dg = pd.read_csv('genele-info-dataframe.csv')
WORDS = list(dg['symbol'])


def normalize_word(w):
    return w.upper().ljust(5)

class Words():
    def __init__(self,word_list=WORDS,sort_by='freq_pos'):
        self.sort_by = sort_by
        self.words = list(map(normalize_word,word_list))
        self.num_words = len(word_list)
        self.freq_by_char = char_frequency(self.words)
        self.freq_by_symb = symbol_frequency(self.words)
        self.freq_by_pos = position_frequency(self.words)

        dw = pd.DataFrame()
        dw['word'] = self.words
        dw['num_distinct'] = dw['word'].apply(lambda w:len(set(w)))
        dw = dw[~dw['word'].str.contains('-')].copy()
        for i in range(0,5):
            dw[f'char{i}'] = dw['word'].apply(lambda x: x[i]).values
        dw['freq_char'] = dw['word'].apply(lambda w:freq_score_sum(w,frequency=self.freq_by_char))
        dw['freq_char_dist'] = dw['word'].apply(lambda w:freq_score_sum_distinct(w,frequency=self.freq_by_char))
        dw['freq_symb'] = dw['word'].apply(lambda w:freq_score_sum(w,frequency=self.freq_by_symb))
        dw['freq_symb_dist'] = dw['word'].apply(lambda w:freq_score_sum_distinct(w,frequency=self.freq_by_symb))
        dw['freq_pos'] = dw['word'].apply(lambda w:freq_score_sum_pos(w,frequency=self.freq_by_pos))
        dw = dw.sort_values(self.sort_by, ascending=False)
        self.table = dw.copy()

    def update(self, guess, feedback):
        guess = normalize_word(guess)
        dw = self.table.copy()
        good_chars = []
        bad_chars = set()
        counter = Counter()
        for i,(x,f) in enumerate(zip(guess,feedback)):
            if f=='2':
                good_chars.append(x)
                counter.update(x)
                dw = dw[dw[f'char{i}'] == x]
            elif f=='1':
                good_chars.append(x)
                counter.update(x)
                dw = dw[dw['word'].str.contains(x.upper())]
                dw = dw[dw[f'char{i}'] != x]
            else:
                bad_chars.add(x)
                
        for x in bad_chars - set(good_chars):
            dw = dw[~dw['word'].str.contains(x.upper())]
        for x in bad_chars & set(good_chars):
            dw = dw[dw['word'].str.count(x) <= counter[x]]
        
        self.freq_by_character = char_frequency(self.words)
        self.freq_by_symb = symbol_frequency(self.words)
        self.freq_by_position = position_frequency(self.words)
        dw['freq_char'] = dw['word'].apply(lambda w:freq_score_sum(w,frequency=self.freq_by_char))
        dw['freq_char_dist'] = dw['word'].apply(lambda w:freq_score_sum_distinct(w,frequency=self.freq_by_char))
        dw['freq_symb'] = dw['word'].apply(lambda w:freq_score_sum(w,frequency=self.freq_by_symb))
        dw['freq_symb_dist'] = dw['word'].apply(lambda w:freq_score_sum_distinct(w,frequency=self.freq_by_symb))
        dw['freq_pos'] = dw['word'].apply(lambda w:freq_score_sum_pos(w,frequency=self.freq_by_pos))
        dw = dw.sort_values(self.sort_by, ascending=False)
        self.table = dw.copy() 
        self.words = sorted(self.table['word'])
        self.num_words = len(self.table)