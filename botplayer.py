from player import Player


class BotPlayer(Player):
    def __init__(self, name, version='v1.0'):
        super().__init__(name)
        self.version = version

    def get_player_card_choice(self):
        if self.version == 'v1.0':
            return self._strategy_v1_0()
        elif self.version == 'v1.1':
            return self._strategy_v1_1()
        elif self.version == 'v1.2':
            return self._strategy_v1_2()
        else:
            return self._strategy_v1_0()

    def _is_legal_play(self, card, top_card):
        if not top_card:
            return True
        if card.value in card.special_values:
            return True
        if top_card.value in top_card.special_values:
            return True
        if top_card.value == '9':
            return card.rank <= 9
        return card.rank >= top_card.rank

    def _find_legal_move(self, top_card):
        print(f"\n{self.name}'s hand: {self.hand}")
        print(f"Top card on pile: {top_card}")

        for i, card in enumerate(self.hand):
            if self._is_legal_play(card, top_card):
                print(f"Choosing to play: {card}")
                return [i]
        print("No legal move found, picking up the pile")
        return -1  # No legal move, pick up the pile

    def _strategy_v1_0(self):
        # Basic strategy: play the first legal card
        top_card = self.game.pile[-1] if self.game.pile else None
        move = self._find_legal_move(top_card)
        if move != -1:
            print(f"{self.name} is playing card: {self.hand[move[0]]}")
        else:
            print(f"{self.name} is picking up the pile")
        return move

    def _strategy_v1_1(self):
        # Improved strategy: play highest legal card or multiple cards of the same value
        self.hand.sort(key=lambda card: card.rank, reverse=True)
        top_card = self.game.pile[-1] if self.game.pile else None

        for i, card in enumerate(self.hand):
            if self._is_legal_play(card, top_card):
                same_value_cards = [j for j, c in enumerate(self.hand) if c.value == card.value]
                if len(same_value_cards) > 1:
                    return same_value_cards
                return [i]

        return -1

    def _strategy_v1_2(self):
        # Advanced strategy: prioritize special cards and consider card counting
        top_card = self.game.pile[-1] if self.game.pile else None
        special_cards = [i for i, card in enumerate(self.hand) if
                         card.value in card.special_values and self._is_legal_play(card, top_card)]
        if special_cards:
            return [special_cards[0]]

        # TODO: Implement card counting logic here

        return self._strategy_v1_1()

    def __repr__(self):
        return f"Bot {self.name} (v{self.version}) has: \n {self.hand} in hand\n {self.table_face_up} face up \n {len(self.table_face_down)} cards face down.\n"