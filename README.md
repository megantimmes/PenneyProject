# PenneyProject

### An Overview of Penney's Game and Two Variations of the Humble-Nishiyama Version

In Penney's Game, two players choose a sequence of heads and tails where the sequence has a length of 3. The player who chooses second must choose a different sequence from that of the player who chooses first. In the game, a fair coin is flipped as many times as is necessary until 3 consecutive flips match the sequence of one of the players, who is the winner of the game. As the coin can be flipped infinitely many times until a player has won, draws are not possible in Penney's game.

In the original variation of the Humble-Nishiyama version, the fair coin is replaced with a standard deck of 52 cards. Instead of picking a sequence of length 3 of heads and tails, players pick separate sequences of black cards and red cards. Like in Penney's Game, cards are drawn from the deck of 52 cards until the colors of 3 consecutive cards match the chosen sequence of one of the players, who is the winner of that "trick." However, unlike in Penney's Game, after 1 trick has been scored, cards are drawn again until no cards remain in the deck. The players are not allowed to change their sequences during the game. Once all cards have been drawn, the player who has won the most tricks is the winner of the game. As it is possible for the players to have won the same number of tricks from a finite deck, the players may draw the original variation of the Humble-Nishiyama version.

In Ron's variation of the Humble-Nishiyama version, cards are drawn as in the original variation. In addition, as in the original variation, when the colors of 3 consecutive cards match the chosen sequence of one of the players, that player wins that hand. Again, the game proceeds until no cards remain in the deck. However, unlike the original variation of the Humble-Nishiyama version, in Ron's version, players do not win or lose the game based on the number of tricks won. Instead, they each count up the cumulative number of cards across the hands they won, and the player who has the most cards is the winner of the game. As it is possible for the players to have won the same number of cards from a finite deck, the players may draw Ron's variation of the Humble-Nishiyama version.


### Directions for Running Code in this Project

To run the code, open the terminal and set the directory to the location of the GitHub repository. Then, enter 

```console
uv run main.py
```

After running main.py as above, the screen will print the number of processed decks and the number of decks waiting to be processed. The user will then be given three options:
- Enter 0 to print the current heatmap
- Enter 1 to add decks
- Enter 2 to process decks
- Enter 3 to end program

When a user enters 0, 1, or 2, they will be able to select another option. For example, the user can print the current heatmap, add decks, process those decks, and print the current heatmap again.


### Project Findings

The results of our project agree with the findings in the original variation of the Humble-Nishiyama version, but slightly differ for Ron's variation. 

In the original variation of the Humble-Nishiyama game, the findings reflect that if player 1 chooses a sequence first, there is an optimal sequence that player 2 can choose to maximize the likelihood of them beating player 1. Here are the possible sequences player 1 can choose followed by the best choices for player 2 in the original variation of the game. Each optimal sequence for player 2 is followed by its win percent (tie percent) over player 1's sequence: 
* BBB -> RBB  ...  99(0)
* BBR -> RBB  ...  94(4)
* BRB -> BBR  ...  80(8)
* BRR -> BBR  ...  88(7)
* RBB -> RRB  ...  88(7)
* RBR -> RRB  ...  80(8)
* RRB -> BRR  ...  94(4)
* RRR -> BRR  ...  99(0)

Player 1 is at a significant disadvantage assuming player 2 chooses the optimal sequence in response to player 1's chosen sequence. However, for player 1 to maximize their odds of winning or tying the game, they should choose either BRB or RBR. For player 2 to find the optimal sequence, they should flip the middle card in player 1's sequence, add it to the start of their sequence, and remove the fourth item in the sequence to end up with an optimal three card sequence.

However, the optimal sequences slightly deviate for Ron's variation of the game. Here are the possible sequences player 1 can choose followed by the best choices for player 2 in Ron's variation of the game. Each optimal sequence for player 2 is followed by its win percent (tie percent) over player 1's sequence:
* BBB -> RBB  ...  100(0)
* BBR -> RBB  ...  100(0)
* BRB -> RRB* ...  94(2)
* BRR -> BBR  ...  95(1)
* RBB -> RRB  ...  95(1)
* RBR -> BBR* ...  94(2)
* RRB -> BRR  ...  100(0)
* RRR -> BRR  ...  100(0)

In the above results, notice that two sequences—-BRB and RBR—-have a star * next to them. These are the sequences for player 1 that have an optimal sequence for player 2 that is different in Ron's variation. When responding to these "alternating" sequences, player 2 should take the middle card and add it twice to the beginning of the sequence, removing the last two cards in the sequence to end up with the optimal three card sequence. For all other player 1 sequences, player 2 can use the same strategy to find the optimal sequence as they would in the original variation. As in the original variation, player 1 is best off choosing BRB or RBR. In Ron's variation, player 1 is at an even greater disadvantage assuming player 2 chooses the optimal sequences in response to player 1.