
from .zone import ZoneHandler, \
        CardToPlay

from .power import PowerHandler, \
        CreatePlayer, \
        NewTurn, TurnStart, \
        ResourcesAvailable, ResourcesUsed

def create_handlers(match, database):
    return [
        CardToPlay(match, database),

        CreatePlayer(match, database),
        NewTurn(match, database),
        TurnStart(match, database),
        ResourcesAvailable(match, database),
        ResourcesUsed(match, database)
    ]
