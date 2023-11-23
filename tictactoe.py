import csv
import os
from datetime import datetime

class Logger:
    def __init__(self, file_name='game_log.csv'):
        self.file_name = file_name
        self.fields = ['timestamp', 'player1', 'player2', 'winner', 'moves']

        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fields)
                writer.writeheader()

    def log_game(self, player1, player2, winner, moves):
        with open(self.file_name, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writerow({
                'timestamp': datetime.now(),
                'player1': player1,
                'player2': player2,
                'winner': winner,
                'moves': moves
            })

import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def move(self, board):
        pass

class HumanPlayer(Player):
    def move(self, board):
        while True:
            try:
                move = input(f"{self.symbol}'s turn. Enter your move (row,col): ")
                row, col = map(int, move.split(","))
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None:
                    return (row, col)
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter the move as row,col. Example: 1,2")

class BotPlayer(Player):
    def move(self, board):
        while True:
            row, col = random.randint(0, 2), random.randint(0, 2)
            if board[row][col] is None:
                return (row, col)
              
class Game:
    def __init__(self, player1, player2):
        self.board = self.make_empty_board()
        self.current_player = player1
        self.other_player = player2
        self.logger = Logger()
        self.move_count = 0

    def make_empty_board(self):
        return [[None, None, None] for _ in range(3)]

    def get_winner(self):
        board = self.board
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]
        return None

    def display_board(self):
        for row in self.board:
            print("|".join([cell if cell is not None else " " for cell in row]))
            print("-" * 5)

    def play_turn(self, player):
        row, col = player.move(self.board)
        self.board[row][col] = player.symbol

    def switch_player(self):
        self.current_player, self.other_player = self.other_player, self.current_player

    def play(self):
        winner = None
        while winner is None:
            self.display_board()
            self.play_turn(self.current_player)
            self.move_count += 1
            winner = self.get_winner()
            if winner is None:
                self.switch_player()
        self.display_board()
        print(f"{winner} has won!")
        self.logger.log_game(self.current_player.symbol, self.other_player.symbol, winner, self.move_count)

if __name__ == '__main__':
    mode = input("Choose game mode (1: single player, 2: two players): ")
    player1 = HumanPlayer("X")
    player2 = BotPlayer("O") if mode == "1" else HumanPlayer("O")
    game = Game(player1, player2)
    game.play()

import pandas as pd
from google.colab import files

log_df = pd.read_csv('game_log.csv')

log_df['moves'] = pd.to_numeric(log_df['moves'])
players = pd.unique(log_df[['player1', 'player2']].values.ravel('K'))

# Initialize DataFrame for wins, losses, and draws
win_loss_draw = pd.DataFrame(index=players, columns=['Wins', 'Losses', 'Draws']).fillna(0)

# Calculate wins and losses for each player
for player in players:
    win_loss_draw.loc[player, 'Wins'] = log_df[log_df['winner'] == player].shape[0]
    win_loss_draw.loc[player, 'Losses'] = log_df[(log_df['player1'] == player) | (log_df['player2'] == player)].shape[0] - win_loss_draw.loc[player, 'Wins']

# Calculate total number of draws
total_draws = log_df[log_df['winner'] == 'D'].shape[0]
win_loss_draw['Draws'] = total_draws

print(win_loss_draw)

# 1. Player Ranks
win_counts = log_df['winner'].value_counts()
player_ranks = win_counts.sort_values(ascending=False)

# 2. Wins/Losses/Draws per Player
loss_counts = log_df[log_df['winner'] != 'D']['winner'].value_counts()
draw_counts = log_df[log_df['winner'] == 'D'].count()[0]
win_loss_draw = pd.DataFrame({'Wins': win_counts, 'Losses': loss_counts, 'Draws': draw_counts})

# 3. Average Play Time to Win (using the number of moves as a proxy for time)
average_moves_to_win = log_df[log_df['winner'] != 'D']['moves'].mean()

# Display the statistics
print("Player Ranks:\n", player_ranks)
print("\nWins/Losses/Draws:\n", win_loss_draw)
print("\nAverage Moves to Win:", average_moves_to_win)

import matplotlib.pyplot as plt

# 1. Number of Wins per Player
win_counts.plot(kind='bar')
plt.title('Number of Wins per Player')
plt.xlabel('Player')
plt.ylabel('Wins')
plt.show()

# 2. Distribution of Moves per Game
log_df['moves'].plot(kind='hist', bins=range(1, log_df['moves'].max() + 1), rwidth=0.8)
plt.title('Distribution of Moves per Game')
plt.xlabel('Number of Moves')
plt.ylabel('Frequency')
plt.show()

# 3. Win/Loss Ratios
print(win_loss_draw)
win_loss_draw = win_loss_draw.fillna(0)
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
win_loss_draw['Wins'].plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Wins')

plt.subplot(1, 2, 2)
win_loss_draw['Losses'].plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Losses')

plt.show()
