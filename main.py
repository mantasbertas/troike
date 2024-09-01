import time
from collections import defaultdict
from game import Game
from botplayer import BotPlayer
import csv

from player import Player


def run_multiple_games(num_games=100, player_names=None, bot_versions=None):
    if player_names is None:
        player_names = ['BotMantas', 'BotJonas', 'BotMartynas']

    if bot_versions is None:
        bot_versions = {name: 'v1.0' for name in player_names}

    stats = {
        'games': [],
        'winners': defaultdict(int),
        'total_turns': 0,
        'total_time': 0
    }

    for i in range(num_games):
        print(f"Starting game {i + 1}/{num_games}")
        game_stats = play_game(player_names, bot_versions)
        stats['games'].append(game_stats)
        stats['winners'][game_stats['winner']] += 1
        stats['total_turns'] += game_stats['turns']
        stats['total_time'] += game_stats['time']

    return stats


def play_game(player_names, bot_versions):
    start_time = time.time()
    players = [BotPlayer(name, bot_versions[name]) if name.startswith("Bot") else Player(name) for name in player_names]
    game = Game(*players)
    game.start_game()

    turns = 0
    while not game.is_game_over():
        game.turn()
        turns += 1

    end_time = time.time()
    game_time = end_time - start_time

    winner = game.active_players[0].name if game.active_players else "No winner"
    winner_version = bot_versions[winner] if winner != "No winner" else "N/A"

    return {
        'winner': winner,
        'winner_version': winner_version,
        'turns': turns,
        'time': game_time
    }


def print_stats(stats):
    print("\nGame Statistics:")
    print(f"Total games played: {len(stats['games'])}")
    print(f"Average turns per game: {stats['total_turns'] / len(stats['games']):.2f}")
    print(f"Average time per game: {stats['total_time'] / len(stats['games']):.2f} seconds")
    print("\nWinners:")
    for winner, count in stats['winners'].items():
        print(f"{winner}: {count} wins ({count / len(stats['games']) * 100:.2f}%)")


def save_stats_to_csv(stats, filename='game_stats.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['game_number', 'winner', 'winner_version', 'turns', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, game in enumerate(stats['games'], 1):
            writer.writerow({
                'game_number': i,
                'winner': game['winner'],
                'winner_version': game['winner_version'],
                'turns': game['turns'],
                'time': game['time']
            })

    print(f"Stats saved to {filename}")


if __name__ == "__main__":
    bot_versions = {
        'BotMantas': 'v1.1',
        'BotJonas': 'v1.1',
        'BotMartynas': 'v1.1'
    }
    stats = run_multiple_games(bot_versions=bot_versions, num_games=10)
    print_stats(stats)
    save_stats_to_csv(stats)
