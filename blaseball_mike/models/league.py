from collections import OrderedDict

from .base import Base
from .team import Team
from .. import database


class League(Base):
    """
    Represents the entire league
    """
    @classmethod
    async def _get_fields(cls):
        p = await cls.load()
        return [cls._from_api_conversion(x) for x in p.fields]

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    async def load(cls):
        return cls(await database.get_league())

    @classmethod
    async def load_by_id(cls, id_):
        return cls(await database.get_league(id_))

    @Base.lazy_load("_subleague_ids", cache_name="_subleagues", default_value=dict())
    async def subleagues(self):
        """Returns dictionary keyed by subleague ID."""
        return {id_: (await Subleague.load(id_)) for id_ in self._subleague_ids}

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for subleague in self.subleagues.values():
            self._teams.update(subleague.teams)
        return self._teams

    @Base.lazy_load("_tiebreakers_id", cache_name="_tiebreaker")
    async def tiebreakers(self):
        return await Tiebreaker.load(self._tiebreakers_id)


class Subleague(Base):
    """
    Represents a subleague, ie Mild vs Wild
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load("4fe65afa-804f-4bb2-9b15-1281b2eab110")
        return [cls._from_api_conversion(x) for x in p.fields]

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    async def load(cls, id_):
        """
        Load by ID.
        """
        return cls(await database.get_subleague(id_))

    @Base.lazy_load("_division_ids", cache_name="_divisions", default_value=dict())
    async def divisions(self):
        """Returns dictionary keyed by division ID."""
        return {id_: (await Division.load(id_)) for id_ in self._division_ids}

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for division in self.divisions.values():
            self._teams.update(division.teams)
        return self._teams


class Division(Base):
    """
    Represents a blaseball division ie Mild Low, Mild High, Wild Low, Wild High.
    """
    @classmethod
    async def _get_fields(cls):
        p = await cls.load("f711d960-dc28-4ae2-9249-e1f320fec7d7")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, id_):
        """
        Load by ID
        """
        return cls(await database.get_division(id_))

    @classmethod
    async def load_all(cls):
        """
        Load all divisions, including historical divisions (Chaotic Good, Lawful Evil, etc.)

        Returns dictionary keyed by division ID.
        """
        return {
            id_: cls(div) for id_, div in (await database.get_all_divisions()).items()
        }

    @classmethod
    async def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        divisions = await cls.load_all()
        for division in divisions.values():
            if name in division.name.lower():
                return division
        return None

    @Base.lazy_load("_team_ids", cache_name="_teams", default_value=dict())
    async def teams(self):
        """
        Comes back as dictionary keyed by team ID
        """
        return {id_: (await Team.load(id_)) for id_ in self._team_ids}


class Tiebreaker(Base):
    """Represents a league's tiebreaker order"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load_one("370c436f-79fa-418b-bc98-5db48442ba3f")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, id_):
        tiebreakers = await database.get_tiebreakers(id_)
        return {
            id_: cls(tiebreaker) for (id_, tiebreaker) in tiebreakers.items()
        }

    @classmethod
    async def load_one(cls, id_):
        return (await cls.load(id_)).get(id_)

    @Base.lazy_load("_order_ids", cache_name="_order", default_value=OrderedDict())
    async def order(self):
        order = OrderedDict()
        for id_ in self._order_ids:
            order[id_] = await Team.load(id_)
        return order
