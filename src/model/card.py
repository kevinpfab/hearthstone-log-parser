
from .base import BaseModel

class Card(BaseModel):
    def __init__(self, card_id, card_data=None):
        self.id = card_id

        self.name = None
        self.set_name = None
        self.cost = 0
        self.type = None
        self.faction = None
        self.text = None
        self.mechanics = []
        self.flavor = None
        self.artist = None
        self.attack = 0
        self.health = 0
        self.collectible = False
        self.elite = False

        if card_data:
            self._set_card_data(card_data)

    def _set_card_data(self, data):
        for key in data:
            if key != 'id':
                setattr(self, key, data[key])

class CardInstance(Card):
    pass

class CardDatabase(BaseModel):

    def __init__(self, data):
        self._database = self._parse_data(data)

    def get_card(self, card_id):
        return self._database.get(card_id)

    def _parse_data(self, data):
        card_database = {}

        for set_name, card_array in data.items():
            for card in card_array:
                c = Card(card['id'], card_data=card)
                c.set_name = set_name

                card_database[c.id] = c

        return card_database



