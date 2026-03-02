import numpy as np
from itertools import permutations
import pandas as pd
from numba import njit 
import os

@njit
def original_deck_score(deck, my_choice, opp_choice):
    my_score = 0
    opp_score = 0
    i = 0
    n = len(deck)
    while i <= n - 3:
        if deck[i] == opp_choice[0] and deck[i+1] == opp_choice[1] and deck[i+2] == opp_choice[2]:
            opp_score += 1
            i += 3
        elif deck[i] == my_choice[0] and deck[i+1] == my_choice[1] and deck[i+2] == my_choice[2]:
            my_score += 1
            i += 3
        else:
            i += 1
    return my_score, opp_score

@njit
def ron_deck_score(deck, my_choice, opp_choice):
    my_score = 0
    opp_score = 0
    i = 0
    n = len(deck)
    cards_since_last = 0
    while i <= n - 3:
        cards_since_last += 1
        if deck[i] == opp_choice[0] and deck[i+1] == opp_choice[1] and deck[i+2] == opp_choice[2]:
            opp_score += cards_since_last
            cards_since_last = 0
            i += 3
        elif deck[i] == my_choice[0] and deck[i+1] == my_choice[1] and deck[i+2] == my_choice[2]:
            my_score += cards_since_last
            cards_since_last = 0
            i += 3
        else:
            i += 1
    return my_score, opp_score


class Data_Process:
    def __init__(self,data):
         
        self.data = data
        self.decks = self.data['saved_decks']
        self.choices = ['000','001','010','011','100','101','110','111'] # the possible choices for each player
        self.choice_arrays = {c: np.array([int(x) for x in c], dtype=np.int8) for c in self.choices}
        def load_or_create_csv(path, choices):
            """Load CSV or create empty DataFrame with given choices."""
            if os.path.isfile(path):
                df = pd.read_csv(path, index_col=0)
                # Ensure labels are strings
                df.index = df.index.astype(str).str.strip()
                df.columns = df.columns.astype(str).str.strip()
                for c in choices:
                    if c not in df.index:
                        df.loc[c] = 0
                    if c not in df.columns:
                        df[c] = 0
                df = df.loc[choices, choices]
                return df.astype(int)
            else:
                return pd.DataFrame(0, index=choices, columns=choices, dtype=int)

        self.wins = load_or_create_csv('data/original_game_wins.csv', self.choices)
        self.draws = load_or_create_csv('data/original_game_draws.csv', self.choices)
        self.ron_wins = load_or_create_csv('data/ron_game_wins.csv', self.choices)
        self.ron_draws = load_or_create_csv('data/ron_game_draws.csv', self.choices)
        
        processed_file = np.load('data/processed.npz')
        processed_decks = processed_file['saved_decks']
        self.games = len(processed_decks)

    def str_to_choice(self, s): #ensures the patterns are in the correct data type
        return np.array([int(c) for c in s], dtype=np.int8)

    
    def process_data(self):
        for deck in self.decks:
            for my_choice_str, opp_choice_str in permutations(self.choices, 2):
                my_choice = self.choice_arrays[my_choice_str]
                opp_choice = self.choice_arrays[opp_choice_str]
                
                my_score, opp_score = original_deck_score(deck, my_choice, opp_choice)
                if my_score > opp_score:
                    self.wins.loc[my_choice_str, opp_choice_str] += 1
                elif my_score == opp_score:
                    self.draws.loc[my_choice_str, opp_choice_str] += 1


                my_score2, opp_score2 = ron_deck_score(deck, my_choice, opp_choice)
                if my_score2 > opp_score2:
                    self.ron_wins.loc[my_choice_str, opp_choice_str] += 1
                elif my_score2 == opp_score2:
                    self.ron_draws.loc[my_choice_str, opp_choice_str] += 1

            self.games += 1

       
        win_pct = self.wins / self.games
        draw_pct = self.draws / self.games

        ron_win_pct = self.ron_wins / self.games
        ron_draw_pct = self.ron_draws / self.games

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

        unprocessed_file = np.load('data/unprocessed.npz')
        unprocessed_decks = unprocessed_file['saved_decks']

        if unprocessed_decks.ndim == 1:
            unprocessed_decks = unprocessed_decks.reshape(-1, 52)

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
