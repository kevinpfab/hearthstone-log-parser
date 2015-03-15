
from .base import BaseModel
from .player import PlayerState
from .event import *

class Turn(BaseModel):

    def __init__(self, number, player=None, start=None):
        self.events = []

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

class TurnState(Turn):

    @staticmethod
    def from_turn(self, turn):
        state = TurnState(turn.number)
        state.player = PlayerState.from_player(turn.player)
        state.start = turn.start

        state.mana_available = turn.mana_available
        state.current_mana = turn.current_mana
        state.total_mana_used = turn.total_mana_used

        state.cards_played = [CardState.from_card_instance(card) for card in turn.cards_played]
