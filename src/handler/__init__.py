
from .zone import ZoneHandler, \
        CardToPlay

from .power import PowerHandler, \
        CreatePlayer, AssignPlayerEntity, \
        NewTurn, TurnStart, \
        ResourcesAvailable, ResourcesUsed, \
        Attacking, Defending, MetaDamage

def create_handlers(match, database):
    return [
        CardToPlay(match, database),

        CreatePlayer(match, database),
        AssignPlayerEntity(match, database),
        NewTurn(match, database),
        TurnStart(match, database),
        ResourcesAvailable(match, database),
        ResourcesUsed(match, database),
        Attacking(match, database),
        Defending(match, database),
        MetaDamage(match, database)
    ]
