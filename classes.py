import random


class Card:
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
              'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    def __init__(self, suite, value):
        self.suite = suite
        self.value = value
        self.rank = Card.values[value]

    def __repr__(self):
        return f"{self.value} of {self.suite}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Card):
            return self.rank < other.rank
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Card):
            return self.rank <= other.rank
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Card):
            return self.rank > other.rank
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Card):
            return self.rank >= other.rank
        return NotImplemented


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.table_face_down = []
        self.table_face_up = []

    def receive_initial_cards(self, deck):
        self.hand = [deck.draw_cards() for _ in range(3)]
        self.table_face_down = [deck.draw_cards() for _ in range(3)]
        self.table_face_up = [deck.draw_cards() for _ in range(3)]

    def draw(self, deck):
        while len(self.hand) < 3 and len(deck) > 0:
            self.hand.append(deck.draw_cards())

    def play_card(self, card):
        self.hand.remove(card)
        return card

    def pick_up_pile(self, pile):
        self.hand.extend(pile)
        pile.clear()


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
                break
            else:
                print("Illegal play. Try again or pick up the pile.")

        print(f"Stack right now is: {self.pile}")
        print(f"Cards remaining in the deck: {len(self.deck)}")

        # Draw cards if necessary
        current_player.draw(self.deck)

        # Move to the next player
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.turn_id += 1

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
