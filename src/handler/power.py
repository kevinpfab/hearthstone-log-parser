
from base import BaseHandler
from tag import PowerTag

from model import Player, Turn

class PowerHandler(BaseHandler):

    def __init__(self, match, database):
        super(PowerHandler, self).__init__(match, database)
        self.base_tag = PowerTag.BASE

    def _execute(self, data):
        pass



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
        new_player = Player(data['value'], data['Entity'])
        self._match.set_player(new_player)

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

# }}}
