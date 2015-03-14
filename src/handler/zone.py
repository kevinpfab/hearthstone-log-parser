
from base import BaseHandler
from tag import ZoneTag

from model import CardInstance

class ZoneHandler(BaseHandler):

    def __init__(self, match, database):
        super(ZoneHandler, self).__init__(match, database)
        self.base_tag = ZoneTag.BASE

    def _execute(self, data):
        pass

class CardToPlay(ZoneHandler):

    def _method(self):
        return ZoneTag.METHOD_CREATE_LOCAL_CHANGES_FROM_TRIGGER

    def _tags(self):
        return [
            ZoneTag.DESTINATION_PLAY
        ]

    def  _execute(self, method, data):
        card = CardInstance(data['localTrigger']['entity']['cardId'])
        card.name = self._database.get_card(card.id).name

        self._match.current_turn.cards_played.append(card)

