from .base import Base
from .team import Team
from .. import database


class Election(Base):
    """Represents the current election"""

    @classmethod
    async def _get_fields(cls):
        p = await cls.load()
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls):
        """Load the current election"""
        offseason = await database.get_offseason_election_details()
        return cls(offseason)

    @Base.lazy_load("_blessings", default_value=list())
    def blessings(self):
        return [Blessing(b) for b in self._blessings]

    @Base.lazy_load("_decrees", default_value=list())
    def decrees(self):
        return [Decree(b) for b in self._decrees]

    @Base.lazy_load("_wills", default_value=list())
    def wills(self):
        return [Will(b) for b in self._wills]

    @Base.lazy_load("_gifts", default_value=list())
    def gifts(self):
        return [Gift(b) for b in self._gifts]


class OffseasonSetup(Election):
    pass


class Decree(Base):
    """Represents a decree currently up for vote"""
    @classmethod
    def _get_fields(cls):
        p = getattr(Election.load(), "decrees", [])
        if len(p) == 0:
            return []
        return [cls._from_api_conversion(x) for x in p.fields]


class Blessing(Base):
    """Represents a blessing currently up for vote"""
    @classmethod
    def _get_fields(cls):
        p = getattr(Election.load(), "blessings", [])
        if len(p) == 0:
            return []
        return [cls._from_api_conversion(x) for x in p.fields]


class Will(Base):
    """Represents a will currently up for vote"""
    @classmethod
    def _get_fields(cls):
        p = getattr(Election.load(), "wills", [])
        if len(p) == 0:
            return []
        return [cls._from_api_conversion(x) for x in p.fields]


class Gift(Base):
    """Represents a gift currently available"""
    @classmethod
    def _get_fields(cls):
        p = getattr(Election.load(), "gifts", [])
        if len(p) == 0:
            return []
        return [cls._from_api_conversion(x) for x in p.fields]


class ElectionResult(Base):
    """Represents the results of an election"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load_by_season(19)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load_by_season(cls, season):
        """
        Load results by season. Season is 1-indexed.
        """
        return cls(await database.get_offseason_recap(season))

    @Base.lazy_load("_bonus_results_ids", cache_name="_bonus_results", default_value=list())
    async def bonus_results(self):
        blessings = await BlessingResult.load(*self._bonus_results_ids)
        return [await blessings.get(id_) for id_ in self._bonus_results_ids]

    # blessing_results is an alias to bonus_results
    @property
    def blessing_results(self):
        return self.bonus_results

    @Base.lazy_load("_decree_results_ids", cache_name="_decree_results", default_value=list())
    async def decree_results(self):
        decrees = await DecreeResult.load(*self._decree_results_ids)
        return[decrees.get(id_) for id_ in self._decree_results_ids]

    @Base.lazy_load("_event_results_ids", cache_name="_event_results", default_value=list())
    async def event_results(self):
        events = await TidingResult.load(*self._event_results_ids)
        return [events.get(id_) for id_ in self._event_results_ids]

    # tiding_results is an alias to event_results
    @property
    def tiding_results(self):
        return self.event_results

    @Base.lazy_load("_season", use_default=False)
    def season(self):
        return self._season + 1


class OffseasonResult(ElectionResult):
    pass


class DecreeResult(Base):
    """Represents the results of a single decree."""
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("643280fc-b7c6-4b6d-a164-9b53e1a3e47a")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls, *ids):
        """
        Load one or more decree results by decree ID
        """
        decrees = database.get_offseason_decree_results(list(ids))
        return {
            id_: cls(decree) for (id_, decree) in decrees.items()
        }

    @classmethod
    def load_one(cls, id_):
        """
        Load a single decree result by decree ID
        """
        return cls.load(id_).get(id_)


class BlessingResult(Base):
    """Represents the results of a single blessing"""
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("cbb567c0-d770-4d22-92f6-ff16ebb94758")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, *ids):
        """
        Load one or more blessing results by blessing ID
        """
        blessings = await database.get_offseason_bonus_results(list(ids))
        return {
            id_: cls(blessing) for (id_, blessing) in blessings.items()
        }

    @classmethod
    async def load_one(cls, id_):
        """
        Load a single blessing result by blessing ID
        """
        return await cls.load(id_).get(id_)

    @Base.lazy_load("_team_id", cache_name="_team")
    async def team_id(self):
        return await Team.load(self._team_id)

    # team is an alias to team_id
    @property
    def team(self):
        return self.team_id

    # Note: highest_team not present for Season 1
    @Base.lazy_load("_highest_team_id", cache_name="_highest_team")
    async def highest_team(self):
        return await Team.load(self._highest_team_id)

    # blessing_title is an alias to bonus_title
    @property
    def blessing_title(self):
        return self.bonus_title

    # blessing_id is an alias to bonus_id
    @property
    def blessing_id(self):
        return self.bonus_id


class BonusResult(BlessingResult):
    pass


class TidingResult(Base):
    """Represents the results of a single election tiding"""
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("future_written")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, *ids):
        event = await database.get_offseason_event_results(list(ids))
        return {
            id_: cls(event) for (id_, event) in event.items()
        }

    @classmethod
    async def load_one(cls, id_):
        return (await cls.load(id_)).get(id_)


class EventResult(TidingResult):
    pass
