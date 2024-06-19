
class Card:
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
              'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    special_values = ['2', '3', '5', '10']

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
