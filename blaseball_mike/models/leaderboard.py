from collections import OrderedDict

from dateutil.parser import parse

from .base import Base
from .player import Player
from .. import database, chronicler


class Idol(Base):
    """Represents a single idol board player"""
    @classmethod
    async def _get_fields(cls):
        p = list((await cls.load()).values())[0]
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls):
        """Load current idol board. Returns ordered dictionary of idols keyed by player ID."""
        idols = await database.get_idols()
        idols_dict = OrderedDict()
        for idol in idols['idols']:
            idols_dict[idol] = cls({"playerId": idol})
        return idols_dict

    @Base.lazy_load("_player_id", cache_name="_player")
    async def player_id(self):
        return await Player.load_one(self._player_id)

    @property
    def player(self):
        return self.player_id


class Tribute(Base):
    """Represents a single tribute recipient on the hall of flame"""
    @classmethod
    async def _get_fields(cls):
        p = list((await cls.load()).values())[0]
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls):
        """Load current hall of flame. Returns ordered dictionary of tributes keyed by player ID."""
        tributes = await database.get_tributes()
        tributes_dict = OrderedDict()
        for tribute in tributes:
            tributes_dict[tribute['playerId']] = cls(tribute)
        return tributes_dict

    @classmethod
    async def load_at_time(cls, time):
        """Load hall of flame at a given time. Returns ordered dictionary of tributes keyed by player ID."""
        if isinstance(time, str):
            time = parse(time)

        tributes = list(await chronicler.get_entities("tributes", at=time))
        tributes_dict = OrderedDict()
        if len(tributes) == 0:
            return tributes_dict
        for tribute in tributes[0]["data"]:
            tributes_dict[tribute['playerId']] = cls(tribute)
        return tributes_dict

    @Base.lazy_load("_player_id", cache_name="_player")
    async def player_id(self):
        if getattr(self, "timestamp", None):
            player = await Player.load_one_at_time(self._player_id, self.timestamp)
            if player is not None:
                return player

            # Due to early archiving issues we do not have accurate data for players incinerated before S2D38. If we
            # cannot find a player at the timestamp passed by the user, instead return the closest data we have and
            # update the player's timestamp accordingly.
            players = await chronicler.get_versions("player", id_=self._player_id, after=self.timestamp, order="asc", count=1)
            if len(players) == 0:
                return None
            player = Player(dict(players[0]["data"], timestamp=players[0]["firstSeen"]))
        else:
            player = Player.load_one(self._player_id)
        return player

    @property
    def player(self):
        return self.player_id
