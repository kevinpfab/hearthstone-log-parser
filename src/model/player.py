
from .base import BaseModel

class Player(BaseModel):

    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name


