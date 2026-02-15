import numpy as np
import os

def data_gen(n: int, # the number of decks to be generated
            ) -> None: # will send the unprocessed decks to be stored in the data folder
    
    '''
    Creates raw data and stores said raw data.
    Raw data consists of decks of 52 cards with 26 blacks (0) and 26 reds (1).
    Deck order is randomized.
    The user may choose how many decks (n) they would like to generate.
    If there is existing data in 'unprocessed.npy', the new decks generated will be added to the decks in 'unprocessed.npy'.
    Should there not be existing data, the new decks are simply stored as 'unprocessed.npy' in the data folder.
    Once the saved unprocessed data is processed, load a zero-element/zero-dimension array to 'unprocessed.npy' as follows:
        np.save('../data/unprocessed.npy', np.array([]))
    '''

    np.random.seed(440) # ensure results are reproducable
    
    blacks = np.zeros(26, dtype=np.int8) # make an array with 26 zeros (blacks)
    reds = np.ones(26, dtype=np.int8) # make an array with 26 ones (reds)
    initial_deck = np.concatenate((blacks, reds)) # join the two arrays to make the initial deck of cards
    
    new_decks = np.array([np.random.permutation(initial_deck) for deck in range(n)]) # make an n x 52 array of randomized decks

    if os.path.isfile('../data/unprocessed.npy'): # if the 'unprocessed.npy' file exists
        unprocessed_decks = np.load('../data/unprocessed.npy') # load the unprocessed_decks
        if len(unprocessed_decks) != 0: # if the unprocessed_decks are not an empty array
            decks_to_save = np.concatenate((unprocessed_decks, new_decks)) # add the new decks to the old unprocessed ones
        else: # if the unprocessed decks are an empty array
            decks_to_save = new_decks # simply prepare the new decks to be saved
    else: # if the 'unprocessed.npy' file does not exist
        decks_to_save = new_decks # simply prepare the new decks to be saved
    # print(len(decks_to_save)) # good way to check if decks are being added correctly

    # Save the decks to 'unprocessed.npy' regardless of if there are already decks there or not
    np.save('../data/unprocessed.npy', decks_to_save)