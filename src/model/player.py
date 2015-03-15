
from .base import BaseModel

class Player(BaseModel):

    def __init__(self, player_id=None, name=None, entity_id=None):
        self.player_id = player_id
        self.name = name
        self.entity_id = entity_id

        self.health = 30

class PlayerState(Player):

    @staticmethod
    def from_player(self, player):
        state = PlayerState(player.player_id, player.name, player.entity_id)
        state.health = player.health

