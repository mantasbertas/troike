import random

from card import Card
from player import Player


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


class Game:
    def __init__(self, *player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.burnt_cards = []
        self.pile = []
        self.turn_id = 0
        self.current_player_idx = 0

    def start_game(self):
        self.deck.shuffle()
        for player in self.players:
            player.receive_initial_cards(self.deck)
            print(f"{player.name}'s hand: {player.hand}")

    def turn(self):
        current_player = self.players[self.current_player_idx]
        print(f"\nIt's {current_player.name}'s turn.")
        print(f"Your hand: {current_player.hand}")

        while True:
            if self.should_pick_up_pile(current_player):
                print(f"{current_player.name} picked up the pile.")
                current_player.pick_up_pile(self.pile)
                break
            card_index = self.get_player_card_choice(current_player)
            if card_index == -1:
                print(f"{current_player.name} picked up the pile.")
                current_player.pick_up_pile(self.pile)
                break
            elif self.is_play_legal(current_player.hand[card_index]):
                played_card = current_player.play_card(current_player.hand[card_index])
                self.pile.append(played_card)
                print(f"{current_player.name} played {played_card}")
                self.check_for_4_in_a_row(self.pile)

                if self.was_special_card_played(played_card):
                    self.special_effect(played_card, current_player)
                break
            else:
                print("Illegal play. Try again or pick up the pile.")

        print(f"Stack right now is: {self.pile}")
        print(f"Cards remaining in the deck: {len(self.deck)}")

        # Draw cards if necessary
        current_player.draw(self.deck)

        # Move to the next player
        if current_player.has_cards():
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            self.turn_id += 1

    def burn_pile(self):
        self.burnt_cards.extend(self.pile)
        self.pile.clear()

    def get_player_card_choice(self, player):
        while True:
            try:
                choice = int(input(f"Choose a card to play (1-{len(player.hand)}) or 0 to pick up the pile: "))
                if choice == 0:
                    return -1  # Indicates the player chose to pick up the pile
                elif 1 <= choice <= len(player.hand):
                    return choice - 1
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input, please enter a number.")

    def is_play_legal(self, card):
        if not self.pile:
            return True
        top_card = self.pile[-1]
        if card.value in card.special_values:
            return True
        return card >= top_card

    def is_game_over(self):
        players_with_cards = sum(1 for player in self.players if self.has_cards(player))
        return players_with_cards <= 1

    def has_cards(self, player):
        return bool(player.hand)
        # return bool(player.hand) or bool(player.table_face_down) or bool(player.table_face_up)

    def should_pick_up_pile(self, player):
        if not self.pile:  # If the pile is empty, any play is legal
            return False
        return not any(self.is_play_legal(card) for card in player.hand)

    def check_for_4_in_a_row(self, pile):
        if len(pile) < 4:
            return
        if all(pile[-1].value == card.value for card in pile[-4:-1]):
            print(f"4 in a row! Pile burns and {self.players[self.current_player_idx].name} takes another turn.")
            self.burn_pile()
            self.current_player_idx = (self.current_player_idx - 1) % len(self.players)

    def was_special_card_played(self, card):
        return card.value in card.special_values

    def special_effect(self, card):
        if card.value == '2':
            # nothing happens we just allow adding from 2 again
            print("Next player can play 2 and up.")
        elif card.value == '3':
            # we find the index of next player, force him to pick up the pile and increment idx by 1

            print("Next player picks up the stack and skips their turn.")
            next_player_idx = (self.current_player_idx + 1) % len(self.players)
            next_player = self.players[next_player_idx]
            next_player.pick_up_pile(self.pile)
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        elif card.value == '5':
            # we decrement the index by 1 so when turn ends it goes back to the same player
            print('He takes another turn!.')
            self.current_player_idx = (self.current_player_idx - 1) % len(self.players)
        elif card.value == '10':
            # we burn the pile
            print("The pile is burned.")
            self.burn_pile()


