#import data
#rrr
#rrb
#rbb
#rbr
#bbb
#brb
#bbr
#brr

#output passed to heatmap should be 4 8x8 arrays 

import numpy as np
from itertools import permutations
import pandas as pd

patterns = ['000','001','010','011','100','101','110','111'] # the possible choices for each player

def str_to_pattern(s): #ensures the patterns are in the correct data type
    return np.array([int(c) for c in s], dtype=np.int8)

def deck_score(deck, pair):
    """
    deck: np.array shape (52,)
    pair: (my_pattern_str, opponent_pattern_str)
    """
    my_choice = str_to_pattern(pair[0])
    opp_choice = str_to_pattern(pair[1])
    my_score = 0
    opponent_score = 0

    i = 0
    n = len(deck)

    while i <= n - 3:
        window = deck[i:i+3]

        if np.array_equal(window, opp_choice):
            opponent_score += 1
            i += 3     #check if the pattern matches opponent choice
        elif np.array_equal(window, my_choice):
            my_score += 1
            i += 3 #check if it matches my choice
        else:
            i += 1         # slide window if no match

    return my_score, opponent_score

def process_data(data):
    labels = patterns

    wins_df = pd.DataFrame(
        0,
        index=labels,
        columns=labels
    )

    for deck in data:
        for pair in permutations(patterns, 2):
            my_choice, opp_choice = pair
            my_score, opp_score = deck_score(deck, pair)

            if my_score > opp_score:
                wins_df.loc[my_choice, opp_choice] += 1

    return wins_df