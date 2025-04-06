# Euclid’s Game – Two-Player Numerical Strategy Game

**Euclid’s Game** is a Sugar activity that implements a turn-based numerical strategy game based on the Euclidean algorithm for finding the greatest common divisor (GCD). In this game, players take turns choosing two numbers from a board and adding their positive difference if it isn’t already present. The game ends when no new number can be added. The winning condition is based on move parity – the player who has made an even number of moves when the game ends is declared the winner.

The educational goal is to familiarize children with the idea behind the Euclidean algorithm (repeated differences) and concepts such as divisors and GCD, all while cultivating strategic thinking and planning skills.

## Features

- **Dynamic Board:**  
  The board starts with two distinct random positive integers (within a chosen range) and gradually grows as players add new numbers (the positive differences).

- **Turn-Based Gameplay:**  
  Players alternate turns. On each turn, a player selects two numbers from the board and, if the positive difference is nonzero and not already on the board, it is added.

- **Move Parity Win Condition:**  
  Unlike traditional games where the last move wins, here the player who makes an even number of moves is declared the winner.

- **Computer Opponent:**  
  In single-player mode, the player competes against a computer AI that chooses moves based on a simple heuristic (e.g., selecting the largest difference).

- **User-Friendly Interface:**  
  The board is displayed using clickable buttons representing each number. Players select two numbers and then click a "Take Difference" button to execute their move. Turn information and move counters for both players are displayed along with game messages.

- **New Game & State Persistence:**  
  A toolbar button allows starting a new game. The activity supports state saving and restoration using Sugar’s `read_file` and `write_file` methods.




## How to Run?


**Running inside Sugar**
- Clone the Repository:
   ```
   git clone https://github.com/ravjot07/FifteenPuzzle
   cd FifteenPuzzle
   ```
-   Open Terminal activity and change to the Fifteen Puzzle activity directory
```
cd \FifteenPuzzle
```

-   To run

```
sugar-activity3 .
```