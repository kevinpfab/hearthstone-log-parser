
from .base import BaseModel

class Match(BaseModel):

    def __init__(self):
        self._players = {}
        self.entities = {}
        self.turns = []

        self._reset_proposed()

    def set_player(self, player):
        if player.player_id in self._players:
            self._players[player.player_id] = player
        else:
            total_players = len(self._players.keys())
            self._players[str(total_players + 1)] = player

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


    def _reset_proposed(self):
        self._proposed_attacking_entity = None
        self._proposed_defending_entity = None
        self._proposed_damage = None

    def attacking(self, attacking_entity=None, damage=None, defending_entity=None):
        if attacking_entity:
            self._proposed_attacking_entity = attacking_entity

        if damage:
            self._proposed_damage = damage

        if defending_entity:
            self._proposed_defending_entity = defending_entity

        if self._proposed_attacking_entity and self._proposed_damage and self._proposed_defending_entity:
            # Resolve attack!
            self._proposed_defending_entity.health = self._proposed_defending_entity.health - int(self._proposed_damage)

            print("%s attacked %s for %s damage" % (self._proposed_attacking_entity.name, \
                                                    self._proposed_defending_entity.name, \
                                                    self._proposed_damage))
            print("Remaining health: %d" % self._proposed_defending_entity.health)

            self._reset_proposed()
