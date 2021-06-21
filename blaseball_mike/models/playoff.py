from .base import Base
from .game import Game
from .team import Team
from .. import database


class Playoff(Base):
    """Represents a playoff bracket"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load_by_season(11)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load_by_season(cls, season):
        """Load playoffs by season. Season is 1-indexed."""
        playoff = await database.get_playoff_details(season)
        return cls(playoff)

    @Base.lazy_load("_rounds_ids", cache_name="_rounds", default_value=list())
    async def rounds(self):
        return [(await PlayoffRound.load(id_)) for id_ in self._rounds_ids]

    def get_round_by_number(self, round_number):
        """
        Get games from a specific round of playoffs. Round number is 1-indexed
        """
        num = round_number - 1
        if num >= len(self._rounds_ids) or num < 0:
            return None
        return self.rounds[num]

    @Base.lazy_load("_winner_id", cache_name="_winner")
    async def winner(self):
        return await Team.load(self._winner_id)

    @Base.lazy_load("_season", use_default=False)
    def season(self):
        return self._season + 1


class PlayoffRound(Base):
    """Represents a round of playoff games"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load("34c99cbf-1d7d-4715-8957-8abcba3c5b89")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, id_):
        """Load round by ID."""
        round_ = await database.get_playoff_round(id_)
        return cls(round_)

    @property
    async def games(self):
        """
        Get all games in this round.
        """
        if all(self._games):
            return self._games
        for day, games in enumerate(self._games_ids):
            if self._games[day]:
                continue
            self._games[day] = [(await Game.load_by_id(id_)) for id_ in games if id_ != "none"]
        return self._games

    @games.setter
    def games(self, value):
        self._games = [None] * len(value)
        self._games_ids = value
        self.key_transform_lookup["games"] = "_games_ids"

    async def get_games_by_number(self, game_number):
        """
        Get games by game number in series (IE: Game 1 of 5). Game number is 1-indexed
        """
        num = game_number - 1
        if num >= len(self._games_ids) or num < 0:
            return []
        if self._games[num]:
            return self._games[num]
        self._games[num] = [(await Game.load_by_id(id_)) for id_ in self._games_ids[num] if id_ != "none"]
        return self._games[num]

    @Base.lazy_load("_matchups_ids", cache_name="_matchups", default_value=list())
    async def matchups(self):
        matchups = await PlayoffMatchup.load(*self._matchups_ids)
        return [matchups.get(id_) for id_ in self._matchups_ids]

    @Base.lazy_load("_winners_ids", cache_name="_winners", default_value=list())
    async def winners(self):
        return [(await Team.load(x)) for x in self._winners_ids]


class PlayoffMatchup(Base):
    """Represents a matchup information of teams in a playoff"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load_one("bee2a1e6-50d6-4866-a7b4-f13705873052")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, *ids_):
        """Load matchup by ID."""
        matchups = await database.get_playoff_matchups(list(ids_))
        return {
            id_: cls(matchup) for (id_, matchup) in matchups.items()
        }

    @classmethod
    async def load_one(cls, id_):
        return (await cls.load(id_)).get(id_)

    @Base.lazy_load("_away_team_id", cache_name="_away_team")
    async def away_team(self):
        return await Team.load(self._away_team_id)

    @Base.lazy_load("_home_team_id", cache_name="_home_team")
    async def home_team(self):
        return await Team.load(self._home_team_id)
