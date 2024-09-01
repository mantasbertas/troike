from player import Player
from botplayer import BotPlayer
from deck import Deck


class Game:
    def __init__(self, *players):
        self.players = []
        for player in players:
            if isinstance(player, str):
                self.players.append(BotPlayer(player) if player.startswith("Bot") else Player(player))
            elif isinstance(player, (Player, BotPlayer)):
                self.players.append(player)
            else:
                raise ValueError(f"Invalid player type: {type(player)}")

        self.deck = Deck()
        self.burnt_cards = []
        self.pile = []
        self.turn_id = 0
        self.current_player_idx = 0
        self.active_players = self.players.copy()

    def start_game(self):
        self.deck.shuffle()
        for player in self.players:
            player.receive_initial_cards(self.deck)
            player.game = self
        print(player)

    def turn(self):
        current_player = self.active_players[self.current_player_idx]
        self.print_turn_info(current_player)

        if self.handle_pick_up_pile(current_player):
            self.finish_turn(current_player)
            return

        while True:
            card_indices = current_player.get_player_card_choice()
            if self.handle_card_play(current_player, card_indices):
                break

        self.finish_turn(current_player)

    def print_turn_info(self, player):
        print(f"\nIt's {player.name}'s turn.")
        print(f"Your hand: {player.hand}")

    def handle_pick_up_pile(self, player):
        if self.should_pick_up_pile(player):
            print(f"No legal moves left, {player.name} picked up the pile.")
            player.pick_up_pile(self.pile)
            return True
        return False

    def handle_card_play(self, player, card_indices):
        if card_indices == -1:
            print(f"{player.name} picked up the pile.")
            player.pick_up_pile(self.pile)
            return True

        if self.is_play_legal(player.hand[card_indices[0]]):
            played_cards = player.play_cards([player.hand[i] for i in card_indices])
            self.pile.extend(played_cards)
            print(f"{player.name} played {played_cards}")

            if played_cards[0].value == '9':
                print(f"Next card is supposed to be lower or equal to 9.")

            if self.check_for_4_in_a_row(self.pile):
                print(f"{player.name} gets another turn!")
                self.current_player_idx = (self.current_player_idx - 1) % len(self.active_players)

            if self.was_special_card_played(played_cards[0]):
                self.special_effect(played_cards[0])

            return True

        print("Illegal play. Try again or pick up the pile.")
        return False

    def finish_turn(self, player):
        print(f"Stack right now is: {self.pile}")
        print(f"Cards remaining in the deck: {len(self.deck)}")

        player.draw(self.deck)

        if not player.has_cards():
            self.eliminate_player(player)

        if self.active_players:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.active_players)
            self.turn_id += 1

    def eliminate_player(self, player):
        print(f"{player.name} has no more cards and is eliminated from the game!")
        self.active_players.remove(player)
        if self.current_player_idx >= len(self.active_players):
            self.current_player_idx = 0

    def burn_pile(self):
        self.burnt_cards.extend(self.pile)
        self.pile.clear()

    def burn_top_3s(self):
        while self.pile and self.pile[-1].value == '3':
            self.burnt_cards.append(self.pile.pop())

    def get_player_card_choice(self, player):
        while True:
            try:
                choice = input(f"Choose cards to play (e.g., 1,2,3) or 0 to pick up the pile: ")
                if choice == '0':
                    return -1  # player chose to pick up the pile
                indices = [int(i) - 1 for i in choice.split(',')]
                if self.are_indices_valid(player, indices):
                    return indices

                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input, please enter a number.")

    @staticmethod
    def are_indices_valid(player, indices):
        """Check if the selected indices are valid (within range and same rank)."""
        return all(0 <= i < len(player.hand) for i in indices) and \
            len(set(player.hand[i].value for i in indices)) == 1

    def is_play_legal(self, card):
        if not self.pile:
            return True
        top_card = self.pile[-1]
        # any special card can be played on any card
        if card.value in card.special_values:
            return True
        # if previous card was special, any card can be played
        if top_card.value in card.special_values:
            return True
        if top_card.value == '9':
            return card <= top_card
        # if selected card is higher or equal to top card, it's legal
        return card >= top_card

    def is_game_over(self):
        if len(self.active_players) <= 1:
            if self.active_players:
                print(f"Game over, {self.active_players[0].name} is the only one with cards remaining. What a loser.")
            else:
                print("Game over, all players have been eliminated.")
            return True
        return False

    def has_cards(self, player):
        return bool(player.hand)  # only need to check hand since we draw before checking
        # return bool(player.hand) or bool(player.table_face_down) or bool(player.table_face_up)

    def should_pick_up_pile(self, player):
        if not self.pile:  # If the pile is empty, any play is legal
            return False
        return not any(self.is_play_legal(card) for card in player.hand)

    def check_for_4_in_a_row(self, pile):
        if len(pile) < 4:
            return False
        if all(pile[-1].value == card.value for card in pile[-4:-1]):
            print(f"4 in a row! Pile burns.")
            self.burn_pile()
            return True
        return False

    def was_special_card_played(self, card):
        return card.value in card.special_values

    def special_effect(self, card):
        if card.value == '2':
            print("Next player can play 2 and up.")
        elif card.value == '3':
            print("Next player picks up the stack and skips their turn.")
            self.burn_top_3s()
            next_player_idx = (self.current_player_idx + 1) % len(self.active_players)
            next_player = self.active_players[next_player_idx]
            next_player.pick_up_pile(self.pile)
            self.current_player_idx = (self.current_player_idx + 1) % len(self.active_players)
        elif card.value == '5':
            print(f"{self.active_players[self.current_player_idx].name} takes another turn!")
            self.current_player_idx = (self.current_player_idx - 1) % len(self.active_players)
        elif card.value == '10':
            print("The pile is burned.")
            self.burn_pile()



