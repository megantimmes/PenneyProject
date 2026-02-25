import numpy as np
import os

def data_gen(n: int # the number of decks to be generated
            ) -> None: # will send the unprocessed decks to be stored in the data folder
    
    '''
    Creates raw data and stores said raw data.
    Raw data consists of decks of 52 cards with 26 blacks (0) and 26 reds (1).
    Deck order is randomized.
    The user may choose how many decks (n) they would like to generate.
    If there is existing data in 'unprocessed.npz', the new decks generated will be added to the decks in 'unprocessed.npz'.
    Should there not be existing data, the new decks are simply stored as 'unprocessed.npy' in the data folder.
    To load the unprocessed data in the data processing file, execute these lines:
        unprocessed_file = np.load('../data/unprocessed.npz')
        unprocessed_decks = unprocessed_file['saved_decks']
    After processing the decks, one could store them as such:
        processed_decks = unprocessed_decks
        np.savez_compressed('../data/processed.npz', saved_decks=processed_decks)
    Once the now processed data is safely stored, load a zero-element/zero-dimension array to 'unprocessed.npz' as follows:
        np.savez_compressed('../data/unprocessed.npz', saved_decks=np.array([]))
    Finally, if these processed decks ever needed to be retrieved, one could execute code similar to the above:
        processed_file = np.load('../data/processed.npz')
        processed_decks = processed_file['saved_decks']
    '''
    
    np.random.seed(440) # ensure results are reproducable
    
    blacks = np.zeros(26, dtype=np.int8) # make an array with 26 zeros (blacks)
    reds = np.ones(26, dtype=np.int8) # make an array with 26 ones (reds)
    initial_deck = np.concatenate((blacks, reds)) # join the two arrays to make the initial deck of cards
    
    new_decks = np.array([np.random.permutation(initial_deck) for deck in range(n)]) # make an n x 52 array of randomized decks

    if os.path.isfile('../data/unprocessed.npz'): # if the 'unprocessed.npz' file exists
        unprocessed_file = np.load('../data/unprocessed.npz') # load the file with the unprocessed decks
        unprocessed_decks = unprocessed_file['saved_decks'] # load the unprocessed decks from said file
        if len(unprocessed_decks) != 0: # if the unprocessed_decks are not an empty array
            decks_to_save = np.concatenate((unprocessed_decks, new_decks)) # add the new decks to the old unprocessed ones
        else: # if the unprocessed decks are an empty array
            decks_to_save = new_decks # simply prepare the new decks to be saved
    else: # if the 'unprocessed.npz' file does not exist
        decks_to_save = new_decks # simply prepare the new decks to be saved
    # print(len(decks_to_save)) # good way to check if decks are being added correctly

    # Save the decks to 'unprocessed.npz' regardless of if there are already decks there or not
    np.savez_compressed('../data/unprocessed.npz', saved_decks=decks_to_save)

def preview_unprocessed(n: int # the number of decks to display
                       ) -> None: # will print the decks to the screen

    '''
    Prints the first few unprocessed decks to the screen.
    '''

    unprocessed_file = np.load('../data/unprocessed.npz')
    unprocessed_decks = unprocessed_file['saved_decks']
    if len(unprocessed_decks) != 0:
        print(unprocessed_decks[:n, :])
    else:
        print('There are no unprocessed decks that are waiting to be processed.')