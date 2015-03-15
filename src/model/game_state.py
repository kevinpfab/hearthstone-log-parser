
from .player import PlayerState

class GameState(object):

    def __init__(self, players=players):
        self.players = players

    @staticmethod
    def freeze(self, match):
        players = [PlayerState.from_player(player) for player in match.player]

        return GameState(players=players)


