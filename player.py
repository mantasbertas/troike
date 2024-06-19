
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
        if len(self.hand) == 0:
            print('No cards left in the deck, picking up face up cards.')
            self.hand.extend(self.table_face_up)
            self.table_face_up.clear()
        if len(self.hand) == 0:
            print('No cards left in the deck, picking up 1 face down card.')

            self.hand.append(self.table_face_down.pop())

    def play_card(self, card):
        self.hand.remove(card)
        return card

    def pick_up_pile(self, pile):
        self.hand.extend(pile)
        pile.clear()

    def has_cards(self):
        return bool(self.hand or self.table_face_down or self.table_face_up)

    def __repr__(self):
        return f"{self.name} has {self.hand} in hand, {len(self.table_face_down)} cards face down, and {self.table_face_up} face up."
