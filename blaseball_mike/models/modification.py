from .base import Base
from .. import database


class Modification(Base):
    """Represents a player or team modification"""
    @classmethod
    async def _get_fields(cls):
        p = await cls.load_one("FIREPROOF")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    async def load(cls, *ids):
        return [cls(mod) for mod in (await database.get_attributes(list(ids)))]

    @classmethod
    async def load_one(cls, id_):
        if id_ in (None, "NONE", ""):
            return None
        return (await cls.load(id_))[0]
