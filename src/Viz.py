import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import pandas as pd

PATH_FIGURES = 'figures'

# Make Heatmap of Game Outcomes

def rb(x):
    '''
    Inputs: a string of 0s and 1s
    Converts 0s and 1s to 'B' and 'R' for heatmap labeling
    '''
    return ''.join('B' if i == '0' else 'R' for i in str(x)) 

def make_figure(filename_org: str, filename_ron: str, games: int) -> None:
    '''
    Inputs:
        filename_org: The original game file will be saved in the default figures folder
        filename2_ron: The Ron's game file will be saved in the default figures folder
    '''

    full_filename_org = os.path.join(PATH_FIGURES, filename_org)
    full_filename_ron = os.path.join(PATH_FIGURES, filename_ron)

    if not os.path.exists(PATH_FIGURES):
        os.mkdir(PATH_FIGURES)
    
    '''
    Original Game Heatmap
    '''
    proc = pd.read_csv('data/original_game_win_pct.csv', dtype={'Unnamed: 0': str}) #read first column as string to keep 3num structure for indexing
    proc = proc.set_index(proc.columns[0]) #Convert first column to index for heatmap plotting
    np.fill_diagonal(proc.values, 0) # Set diagonal to 0 from NAN for greying heatmap diagonal

    t_proc = pd.read_csv('data/original_game_draw_pct.csv', dtype={'Unnamed: 0': str})
    t_proc = t_proc.set_index(t_proc.columns[0])
    np.fill_diagonal(t_proc.values, 0) 

    fig, ax = plt.subplots(1,1, figsize=(6,6))
    annot = np.full(shape=proc.shape, fill_value='', dtype='<U10')  
    for i in range(annot.shape[0]):
        for j in range(annot.shape[1]):
            annot[i, j] = f'{round(proc.iloc[i,j]*100)} ({round(t_proc.iloc[i,j]*100)})' #create annotation for cells "win% (draw%)" from each seperate heatmap
    mask = np.zeros_like(proc, dtype=bool) #create mask to grey diagonal
    np.fill_diagonal(mask, True) #implement mask to grey diagonal
    ax = sns.heatmap(data=proc, cmap='Blues', mask=mask, annot=annot, fmt="",
                    cbar=False, linewidth=.5, square=True) #create heatmap
    ax.set_facecolor('grey') #set grey background for masked diagonal
    ax.set_xticklabels([rb(i.get_text()) for i in ax.get_xticklabels()]) #change x and y labels to 'B' and 'R' from 0s and 1s
    ax.set_yticklabels([rb(i.get_text()) for i in ax.get_yticklabels()])
    plt.xlabel("My Choice") 
    plt.ylabel("Opponent Choice") 
    plt.title(f'My Chance of Win(Draw)\nBy Tricks\nN={games}') #Make sure to change to proper varialbe
    plt.savefig(full_filename_org, bbox_inches='tight')
    plt.show()

    '''
    Ron's Game 
    '''

    games= pd.read_csv('data/games.csv') 
    games= games.iloc[0,1] #get number of games from csv for title

    proc = pd.read_csv('data/ron_game_win_pct.csv', dtype={'Unnamed: 0': str}) #read first column as string to keep 3num structure for indexing
    proc = proc.set_index(proc.columns[0]) #Convert first column to index for heatmap plotting
    np.fill_diagonal(proc.values, 0) # Set diagonal to 0 from NAN for greying heatmap diagonal

    t_proc = pd.read_csv('data/ron_game_draw_pct.csv', dtype={'Unnamed: 0': str})
    t_proc = t_proc.set_index(t_proc.columns[0])
    np.fill_diagonal(t_proc.values, 0) 

    fig, ax = plt.subplots(1,1, figsize=(6,6))
    annot = np.full(shape=proc.shape, fill_value='', dtype='<U10')  
    for i in range(annot.shape[0]):
        for j in range(annot.shape[1]):
            annot[i, j] = f'{round(proc.iloc[i,j]*100)} ({round(t_proc.iloc[i,j]*100)})' #create annotation for cells "win% (draw%)" from each seperate heatmap
    mask = np.zeros_like(proc, dtype=bool) #create mask to grey diagonal
    np.fill_diagonal(mask, True) #implement mask to grey diagonal
    ax = sns.heatmap(data=proc, cmap='Blues', mask=mask, annot=annot, fmt="",
                    cbar=False, linewidth=.5, square=True) #create heatmap
    ax.set_facecolor('grey') #set grey background for masked diagonal
    ax.set_xticklabels([rb(i.get_text()) for i in ax.get_xticklabels()]) #change x and y labels to 'B' and 'R' from 0s and 1s
    ax.set_yticklabels([rb(i.get_text()) for i in ax.get_yticklabels()])
    plt.xlabel("My Choice") 
    plt.ylabel("Opponent Choice") 
    plt.title(f'My Chance of Win(Draw)\nBy Cards\nN={games}') #Make sure to change to proper varialbe
    plt.savefig(full_filename_ron, bbox_inches='tight')
    plt.show()

    return None