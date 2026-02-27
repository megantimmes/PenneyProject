#import data

import numpy as np
from itertools import permutations
import pandas as pd


class Data_Process:
    def __init__(self,data):
        self.data = data
        #self.decks = self.data['saved_decks']
        self.choices = ['000','001','010','011','100','101','110','111'] # the possible choices for each player
        self.wins = pd.DataFrame(
            0,
            index=self.choices,
            columns=self.choices
        )

        self.draws = pd.DataFrame(
            0,
            index=self.choices,
            columns=self.choices
        )

        self.ron_wins = pd.DataFrame(
            0,
            index=self.choices,
            columns=self.choices
        )

        self.ron_draws = pd.DataFrame(
            0,
            index=self.choices,
            columns=self.choices
        )
        self.games = pd.DataFrame(0, index=self.choices, columns=self.choices)

    def str_to_choice(self, s): #ensures the patterns are in the correct data type
        return np.array([int(c) for c in s], dtype=np.int8)

    def original_deck_score(self, deck, pair):
        """
        deck: np.array shape (52,)
        pair: (my_pattern_str, opponent_pattern_str)
        """
        my_choice = self.str_to_choice(pair[0])
        opp_choice = self.str_to_choice(pair[1])
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
    

    def ron_deck_score(self, deck, pair):
        my_choice = self.str_to_choice(pair[0])
        opp_choice = self.str_to_choice(pair[1])

        my_score = 0
        opponent_score = 0

        cards_since_last_match = 0

        i = 0
        n = len(deck)

        while i <= n - 3:
            window = deck[i:i+3]
            cards_since_last_match += 1  

            if np.array_equal(window, opp_choice):
                opponent_score += cards_since_last_match
                cards_since_last_match = 0
                i += 3
            elif np.array_equal(window, my_choice):
                my_score += cards_since_last_match
                cards_since_last_match = 0
                i += 3
            else:
                i += 1

        return my_score, opponent_score

    def process_data(self):
        for deck in self.data:
            for pair in permutations(self.choices, 2):
                my_choice, opp_choice = pair
                my_score, opp_score = self.original_deck_score(deck, pair)

                my_score2, opp_score2 = self.ron_deck_score(deck, pair)

                self.games.loc[my_choice, opp_choice] += 1

                if my_score > opp_score:
                    self.wins.loc[my_choice, opp_choice] += 1
                elif my_score == opp_score:
                    self.draws.loc[my_choice, opp_choice] += 1

                if my_score2 > opp_score2:
                    self.ron_wins.loc[my_choice, opp_choice] += 1
                elif my_score2 == opp_score2:
                    self.ron_draws.loc[my_choice, opp_choice] += 1

       
        win_pct = self.wins / self.games
        draw_pct = self.draws / self.games

        ron_win_pct = self.ron_wins / self.games
        ron_draw_pct = self.ron_draws / self.games

        win_pct.to_csv('data/original_game_win_pct.csv')
        draw_pct.to_csv('data/original_game_draw_pct.csv')
        ron_win_pct.to_csv('data/ron_game_win_pct.csv')
        ron_draw_pct.to_csv('data/ron_game_draw_pct.csv')

        return 


n = 20
np.random.seed(440) # ensure results are reproducable

blacks = np.zeros(26, dtype=np.int8) # make an array with 26 zeros (blacks)
reds = np.ones(26, dtype=np.int8) # make an array with 26 ones (reds)
initial_deck = np.concatenate((blacks, reds)) # join the two arrays to make the initial deck of cards

new_decks = np.array([np.random.permutation(initial_deck) for deck in range(n)])
process = Data_Process(new_decks)
process.process_data()