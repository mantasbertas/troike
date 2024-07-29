import random
from card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.populate_deck()

    def populate_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suite in suits:
            for value in values:
                self.cards.append(Card(suite, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_cards(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)