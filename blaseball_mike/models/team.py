from dateutil.parser import parse

from .base import Base
from .modification import Modification
from .player import Player
from .stadium import Stadium
from .. import database, chronicler, tables


class Team(Base):
    """
    Represents a blaseball team.
    """
    @classmethod
    async def _get_fields(cls):
        p = await cls.load("8d87c468-699a-47a8-b40d-cfb73a5660ad")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, id_):
        """
        Load team by ID.
        """
        return cls(await database.get_team(id_))

    @classmethod
    async def load_all(cls):
        """
        Load all teams, including historical and tournament teams. Currently does not include the PODs.

        Returns dictionary keyed by team ID.
        """
        return {
            id_: cls(team) for id_, team in (await database.get_all_teams()).items()
        }

    @classmethod
    async def load_history(cls, id_, order='desc', count=None):
        """
        Returns array of Team changes with most recent first.
        """
        teams = await chronicler.get_versions("team", id_=id_, order=order, count=count)
        return [cls(dict(p['data'], timestamp=p['validFrom'])) for p in teams]

    @classmethod
    async def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        teams = (await cls.load_all()).values()
        name = name.lower()
        for team in teams:
            if name in team.full_name.lower():
                return team
        return None

    @classmethod
    async def load_at_time(cls, id_, time):
        """
        Load blaseball team with roster at given datetime.
        """
        if isinstance(time, str):
            time = parse(time)

        team = list(await chronicler.get_entities("team", id_, at=time))
        if len(team) == 0:
            return None
        return cls(dict(team[0]["data"], timestamp=time))

    @Base.lazy_load("_lineup_ids", cache_name="_lineup", default_value=list())
    async def lineup(self):
        if getattr(self, "timestamp", None):
            return [(await Player.load_one_at_time(x, self.timestamp)) for x in self._lineup_ids]
        else:
            players = await Player.load(*self._lineup_ids)
            return [players.get(id_) for id_ in self._lineup_ids]

    @Base.lazy_load("_rotation_ids", cache_name="_rotation", default_value=list())
    async def rotation(self):
        if getattr(self, "timestamp", None):
            return [(await Player.load_one_at_time(x, self.timestamp)) for x in self._rotation_ids]
        else:
            players = await Player.load(*self._rotation_ids)
            return [players.get(id_) for id_ in self._rotation_ids]

    @Base.lazy_load("_bullpen_ids", cache_name="_bullpen", default_value=list())
    async def bullpen(self):
        if getattr(self, "timestamp", None):
            return [(await Player.load_one_at_time(x, self.timestamp)) for x in self._bullpen_ids]
        else:
            players = await Player.load(*self._bullpen_ids)
            return [players.get(id_) for id_ in self._bullpen_ids]

    @Base.lazy_load("_bench_ids", cache_name="_bench", default_value=list())
    async def bench(self):
        if getattr(self, "timestamp", None):
            return [(await Player.load_one_at_time(x, self.timestamp)) for x in self._bench_ids]
        else:
            players = await Player.load(*self._bench_ids)
            return [players.get(id_) for id_ in self._bench_ids]

    @Base.lazy_load("_perm_attr_ids", cache_name="_perm_attr", default_value=list())
    async def perm_attr(self):
        return await Modification.load(*self._perm_attr_ids)

    @Base.lazy_load("_seas_attr_ids", cache_name="_seas_attr", default_value=list())
    async def seas_attr(self):
        return await Modification.load(*self._seas_attr_ids)

    @Base.lazy_load("_week_attr_ids", cache_name="_week_attr", default_value=list())
    async def week_attr(self):
        return await Modification.load(*self._week_attr_ids)

    @Base.lazy_load("_game_attr_ids", cache_name="_game_attr", default_value=list())
    async def game_attr(self):
        return await Modification.load(*self._game_attr_ids)

    @Base.lazy_load("_card")
    async def card(self):
        return tables.Tarot(self._card)

    @Base.lazy_load("_stadium_id", cache_name="_stadium")
    async def stadium(self):
        if self._stadium_id is None:
            return None
        return await Stadium.load_one(self._stadium_id)
