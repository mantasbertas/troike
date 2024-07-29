
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.table_face_down = []
        self.table_face_up = []
        # self.rank_counts = {}

    def receive_initial_cards(self, deck):
        self.hand = [deck.draw_cards() for _ in range(3)]
        self.table_face_down = [deck.draw_cards() for _ in range(3)]
        self.table_face_up = [deck.draw_cards() for _ in range(3)]
        self.sort_hand()

        # self.update_hand_counts()

    def draw(self, deck):
        while len(self.hand) < 3 and len(deck) > 0:
            self.hand.append(deck.draw_cards())
        if len(self.hand) == 0:
            print('No cards left in the deck, picking up face up cards.')
            self.hand.extend(self.table_face_up)
            self.table_face_up.clear()
        if len(self.hand) == 0 and self.table_face_down:
            print('No cards left in the deck, picking up 1 face down card.')
            self.hand.append(self.table_face_down.pop())
        self.sort_hand()

    def play_cards(self, cards):
        for card in cards:
            self.hand.remove(card)
        # self.update_hand_counts()
        return cards

    def pick_up_pile(self, pile):
        self.hand.extend(pile)
        # self.update_hand_counts()
        self.sort_hand()
        pile.clear()

    def has_cards(self):
        return bool(self.hand or self.table_face_down or self.table_face_up)

    def sort_hand(self):
        self.hand.sort(key=lambda card: card.rank)

    # def update_hand_counts(self):
    #     self.rank_counts = {}
    #     for card in self.hand:
    #         if card.rank in self.rank_counts:
    #             self.rank_counts[card.rank] += 1
    #         else:
    #             self.rank_counts[card.rank] = self.rank_counts.get(card.rank, 0) + 1

    def get_player_card_choice(self):
        while True:
            try:
                choice = input(f"Choose cards to play (e.g., 1,2,3) or 0 to pick up the pile: ")
                if choice == '0':
                    return -1  # Indicates the player chose to pick up the pile
                indices = [int(i) - 1 for i in choice.split(',')]
                if self.are_indices_valid(indices):
                    return indices
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input, please enter numbers separated by commas.")

    def are_indices_valid(self, indices):
        """Check if the selected indices are valid (within range and same rank)."""
        return all(0 <= i < len(self.hand) for i in indices) and \
            len(set(self.hand[i].value for i in indices)) == 1

    def __repr__(self):
        return f"{self.name} has: \n {self.hand} in hand\n {self.table_face_up} face up \n {len(self.table_face_down)} cards face down.\n"
