
from .base import BaseModel

class Match(BaseModel):

    def __init__(self):
        self._players = {}
        self.turns = []

    def set_player(self, player):
        self._players[player.id] = player

    def get_player(self, player_id):
        return self._players[str(player_id)]

    def get_player_by_name(self, name):
        for player in self._players.values():
            if player.name == name:
                return player

    def get_turn(self, turn_number):
        return self.turns[int(turn_number)]

    @property
    def current_turn(self):
        return self.turns[-1]


