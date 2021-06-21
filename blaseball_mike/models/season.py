from .base import Base
from .league import League
from .statsheet import SeasonStatsheet
from .. import database


class Season(Base):
    """Represents an individual season"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load(11)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, season_number):
        """Load season by season number. Season number is 1-indexed"""
        season = await database.get_season(season_number)
        return cls(season)

    @Base.lazy_load("_league_id", cache_name="_league")
    async def league(self):
        return await League.load_by_id(self._league_id)

    @Base.lazy_load("_standings_id", cache_name="_standings")
    async def standings(self):
        return await Standings.load(self._standings_id)

    @Base.lazy_load("_stats_id", cache_name="_stats")
    async def stats(self):
        return (await SeasonStatsheet.load(self._stats_id))[self._stats_id]

    @Base.lazy_load("_season_number", use_default=False)
    def season_number(self):
        return self._season_number + 1


class Standings(Base):
    """Represents the team standings"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load("dbcb0a13-2d59-4f13-8681-fd969aefdcc6")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, id_):
        """Load standings by ID"""
        standings = await database.get_standings(id_)
        return cls(standings)

    def get_standings_by_team(self, id_):
        """Returns a dictionary of wins & losses of a single team"""
        return {"wins": self.wins.get(id_, None), "losses": self.losses.get(id_, None)}
