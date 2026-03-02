import numpy as np
from itertools import permutations
import pandas as pd
import os


class Data_Process:
    def __init__(self,data):
        self.data = data
        self.decks = self.data['saved_decks']
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
        for deck in self.decks:
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

        self.games.to_csv('data/games.csv')

        self.wins.to_csv('data/original_game_wins.csv')
        self.draws.to_csv('data/original_game_draws.csv')
        self.ron_wins.to_csv('data/ron_game_wins.csv')
        self.ron_draws.to_csv('data/ron_game_draws.csv')

        win_pct.to_csv('data/original_game_win_pct.csv')
        draw_pct.to_csv('data/original_game_draw_pct.csv')
        ron_win_pct.to_csv('data/ron_game_win_pct.csv')
        ron_draw_pct.to_csv('data/ron_game_draw_pct.csv')

        self.finalize_processing()
        return 
    
    def finalize_processing(self):

        # Load unprocessed decks
        unprocessed_file = np.load('data/unprocessed.npz')
        unprocessed_decks = unprocessed_file['saved_decks']

        # Ensure unprocessed is 2D
        if unprocessed_decks.ndim == 1:
            unprocessed_decks = unprocessed_decks.reshape(-1, 52)

        # Load processed decks safely
        if os.path.isfile('data/processed.npz'):
            try:
                processed_file = np.load('data/processed.npz')
                old_processed = processed_file['saved_decks']

                if old_processed.ndim == 1:
                    old_processed = old_processed.reshape(-1, 52)

            except:
                old_processed = np.empty((0, 52), dtype=np.int8)
        else:
            old_processed = np.empty((0, 52), dtype=np.int8)

        # Concatenate safely
        if old_processed.size == 0:
            decks_to_save = unprocessed_decks
        elif unprocessed_decks.size == 0:
            decks_to_save = old_processed
        else:
            decks_to_save = np.concatenate(
                (old_processed, unprocessed_decks),
                axis=0
            )

        # Save processed decks
        np.savez_compressed(
            'data/processed.npz',
            saved_decks=decks_to_save
        )

        # Clear unprocessed safely
        np.savez_compressed(
            'data/unprocessed.npz',
            saved_decks=np.empty((0, 52), dtype=np.int8)
        )
