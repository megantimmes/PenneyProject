from src.data_process import Data_Process
from src.data_gen import data_gen
from src.Viz import make_figure
import numpy as np
import os

while(True):
    if os.path.isfile('data/processed.npz'):
        processed_file = np.load('data/processed.npz')
        processed_decks = processed_file['saved_decks']
    else:
        processed_decks = np.array([])

    if os.path.isfile('data/unprocessed.npz'):
        unprocessed_file = np.load('data/unprocessed.npz')
        unprocessed_decks = unprocessed_file['saved_decks']
    else:
        unprocessed_decks = np.array([])
 
    processed_number = len(processed_decks)
    unprocessed_number = len(unprocessed_decks)


    print(f'There are currently {processed_number} processed decks.')
    print(f'There are currently {unprocessed_number} decks waiting to be processed.')
    print('Enter 0 to print the current heatmap')
    print('Enter 1 to add decks')
    choice = int(input('Enter 2 to process decks '))
    
    if choice == 0:
        make_figure('original', 'ron')
    elif choice == 1:
        n = int(input('How many decks? '))
        data_gen(n)
    elif choice == 2:
        processor = Data_Process(unprocessed_file)
        processor.process_data()
        processor.finalize_processing()
        print('Processed!')

    elif choice == 3:
        np.savez_compressed(
            'data/unprocessed.npz',
            saved_decks=np.empty((0, 52), dtype=np.int8)
        )
        np.savez_compressed(
            'data/processed.npz',
            saved_decks=np.empty((0, 52), dtype=np.int8)
        )


    else:
        print('Not a valid input. Please try again.')
