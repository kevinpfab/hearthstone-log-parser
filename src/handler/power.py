
from helpers import Helpers

from base import BaseHandler
from tag import PowerTag

from model import Player, Turn

class PowerHandler(BaseHandler):

    def __init__(self, match, database):
        super(PowerHandler, self).__init__(match, database)
        self.base_tag = PowerTag.BASE

    def _execute(self, data):
        pass

class MetaDamage(PowerHandler):

    def _tags(self):
        return [PowerTag.META_DAMAGE]

    def _execute(self, method, data):
        self._match.attacking(damage=data['Data'])

# Tag Change lines only have 1 tag that's associated via a "tag="
# {{{ Tag Change Handlers
class TagChange(PowerHandler):

    def _check_tags(self, s):
        rest = (PowerTag.TAG_CHANGE in s) and (("tag=%s " % self._tag()) in s)
        return rest

    def _tag(self):
        pass

class CreatePlayer(TagChange):

    def _tag(self):
        return PowerTag.PLAYER_ID

    def _execute(self, method, data):
        player = self._match.get_player_by_name(data['Entity'])
        if not player:
            player = Player(name=data['Entity'], entity_id=data['value'])
            self._match.set_player(player)

        player.player_id = data['value']

class AssignPlayerEntity(TagChange):

    def _tag(self):
        return PowerTag.HERO_ENTITY

    def _execute(self, method, data):
        player = self._match.get_player_by_name(data['Entity'])
        if not player:
            player = Player(name=data['Entity'], entity_id=data['value'])
            self._match.set_player(player)

        player.entity_id = data['value']
        self._match.entities[player.entity_id] = player

class NewTurn(TagChange):

    def _tag(self):
        return PowerTag.TURN

    def _execute(self, method, data):
        new_turn = Turn(data['value'])
        self._match.turns.append(new_turn)

class TurnStart(TagChange):

    def _tag(self):
        return PowerTag.TURN_START

    def _execute(self, method, data):
        entity = data['Entity']
        if entity != 'GameEntity':
            self._match.current_turn.player = self._match.get_player_by_name(entity)
            self._match.current_turn.start = int(data['value'])

class ResourcesAvailable(TagChange):

    def _tag(self):
        return PowerTag.RESOURCES

    def _execute(self, method, data):
        self._match.current_turn.set_mana_available(int(data['value']))

class ResourcesUsed(TagChange):

    def _tag(self):
        return PowerTag.RESOURCES_USED

    def _execute(self, method, data):
        self._match.current_turn.total_mana_used = int(data['value'])

class Attacking(TagChange):
    def _tag(self):
        return PowerTag.ATTACKING

    def _execute(self, method, data):
        if data['value'] == '1':
            entity = self._match.entities[data['Entity']['id']]
            self._match.attacking(attacking_entity=entity)

class Defending(TagChange):
    def _tag(self):
        return PowerTag.DEFENDING

    def _execute(self, method, data):
        if data['value'] == '1':
            entity = self._match.entities[data['Entity']['id']]
            self._match.attacking(defending_entity=entity)


# }}}
