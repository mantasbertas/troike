from player import Player
from botplayer import BotPlayer
from deck import Deck


class Game:
    def __init__(self, *player_names):
        self.players = [BotPlayer(name) if name.startswith("Bot") else Player(name) for name in player_names]
        self.deck = Deck()
        self.burnt_cards = []
        self.pile = []
        self.turn_id = 0
        self.current_player_idx = 0

    def start_game(self):
        self.deck.shuffle()
        for player in self.players:
            player.receive_initial_cards(self.deck)
            print(player)

    def turn(self):
        current_player = self.players[self.current_player_idx]
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
            print(f"{player.name} picked up the pile.")
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

            self.check_for_4_in_a_row(self.pile)

            if self.was_special_card_played(played_cards[0]):
                self.special_effect(played_cards[0])

            return True

        print("Illegal play. Try again or pick up the pile.")
        return False

    def finish_turn(self, player):
        print(f"Stack right now is: {self.pile}")
        print(f"Cards remaining in the deck: {len(self.deck)}")

        player.draw(self.deck)

        if player.has_cards():
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            self.turn_id += 1

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
        if top_card.values in card.special_values:
            return True
        if top_card.value == '9':
            return card <= top_card
        # if selected card is higher or equal to top card, it's legal
        return card >= top_card

    def is_game_over(self):
        players_with_cards = sum(1 for player in self.players if self.has_cards(player))
        if players_with_cards <= 1:
            for player in self.players:
                if player.has_cards():
                    print(f"Game over, {player.name} is the only one with cards remaining. What a loser.")
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
            self.burn_top_3s()
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


