
from .base import BaseModel

class Turn(BaseModel):

    def __init__(self, number, player=None, start=None):
        self.number = number
        self.player = player
        self.start = start

        self.mana_available = 0
        self.current_mana = 0
        self.total_mana_used = 0

        self.cards_played = []

    def set_mana_available(self, mana):
        self.mana_available = mana
        self.current_mana = mana

