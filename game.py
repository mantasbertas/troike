from classes import *

deck = Deck()
print("Deck before shuffling:")
print(deck.cards)

deck.shuffle()
print("\nDeck after shuffling:")
print(deck.cards)

card_drawn = deck.draw_cards()
print(f"\nCard drawn: {card_drawn}")
print(f"\nRemaining cards in the deck: {len(deck)}")
print("\nDeck after drawing:")
print(deck.cards)


def play_game():
    # player_names = input("Enter player names, separated by space: ").split()
    player_names = ['Mantas', 'Jonas', 'Martynas']
    game = Game(*player_names)
    game.start_game()

    while not game.is_game_over():
        game.turn()

    print("Game over!")

play_game()
