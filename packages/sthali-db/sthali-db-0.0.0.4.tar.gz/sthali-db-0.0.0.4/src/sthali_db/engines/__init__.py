import importlib
from typing import Any

from ..types import DBSpecification
from .base import BaseEngine


class DBEngine(BaseEngine):
    engine: BaseEngine

    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        engine_module = importlib.import_module(f".{db_spec.engine.lower()}", package=__package__)
        engine_class: type[BaseEngine] = getattr(engine_module, f"{db_spec.engine}Engine")
        self.engine = engine_class(db_spec.path, table)

    async def db_insert_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_insert_one(*args, **kwargs)

    async def db_select_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_select_one(*args, **kwargs)

    async def db_update_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_update_one(*args, **kwargs)

    async def db_delete_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_delete_one(*args, **kwargs)

    async def db_select_all(self, *args, **kwargs) -> Any:
        return await self.engine.db_select_all(*args, **kwargs)
