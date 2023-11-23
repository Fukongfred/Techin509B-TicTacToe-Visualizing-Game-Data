import pandas as pd
import matplotlib.pyplot as plt
from logic import Game, HumanPlayer, BotPlayer

def main():
    mode = input("Choose game mode (1: single player, 2: two players): ")
    player1 = HumanPlayer("X")
    player2 = BotPlayer("O") if mode == "1" else HumanPlayer("O")
    game = Game(player1, player2)
    game.play()

    analyze_game_data()

def analyze_game_data():
    log_df = pd.read_csv('game_log.csv')
    log_df['moves'] = pd.to_numeric(log_df['moves'])

    players = pd.unique(log_df[['player1', 'player2']].values.ravel('K'))
    win_loss_draw = pd.DataFrame(index=players, columns=['Wins', 'Losses', 'Draws']).fillna(0)

    for player in players:
        win_loss_draw.loc[player, 'Wins'] = log_df[log_df['winner'] == player].shape[0]
        win_loss_draw.loc[player, 'Losses'] = log_df[(log_df['player1'] == player) | (log_df['player2'] == player)].shape[0] - win_loss_draw.loc[player, 'Wins']

    total_draws = log_df[log_df['winner'] == 'D'].shape[0]
    win_loss_draw['Draws'] = total_draws

    # Player Ranks
    win_counts = log_df['winner'].value_counts()
    player_ranks = win_counts.sort_values(ascending=False)

    # Wins/Losses/Draws per Player
    loss_counts = log_df[log_df['winner'] != 'D']['winner'].value_counts()
    draw_counts = log_df[log_df['winner'] == 'D'].count()[0]
    win_loss_draw = pd.DataFrame({'Wins': win_counts, 'Losses': loss_counts, 'Draws': draw_counts})

    # Average Play Time to Win
    average_moves_to_win = log_df[log_df['winner'] != 'D']['moves'].mean()

    # Display the statistics
    print("Player Ranks:\n", player_ranks)
    print("\nWins/Losses/Draws:\n", win_loss_draw)
    print("\nAverage Moves to Win:", average_moves_to_win)

    # Plotting
    win_counts.plot(kind='bar')
    plt.title('Number of Wins per Player')
    plt.xlabel('Player')
    plt.ylabel('Wins')
    plt.show()

    log_df['moves'].plot(kind='hist', bins=range(1, log_df['moves'].max() + 1), rwidth=0.8)
    plt.title('Distribution of Moves per Game')
    plt.xlabel('Number of Moves')
    plt.ylabel('Frequency')
    plt.show()

    win_loss_draw = win_loss_draw.fillna(0)
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    win_loss_draw['Wins'].plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Wins')

    plt.subplot(1, 2, 2)
    win_loss_draw['Losses'].plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Losses')

    plt.show()

if __name__ == '__main__':
    main()
