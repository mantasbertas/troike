import random
from player import Player


class BotPlayer(Player):
    def get_player_card_choice(self):  # plays random cards
        if not self.hand:
            return -1  # Indicates the bot should pick up the pile
        card_value = random.choice(self.hand).value
        indices = [i for i, card in enumerate(self.hand) if card.value == card_value]
        return indices

    def __repr__(self):
        return f"Bot {self.name} has {self.hand} in hand, {len(self.table_face_down)} cards face down, and {self.table_face_up} face up."

