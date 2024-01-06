from uuid import UUID

from pydantic import NonNegativeInt

from .base import BaseEngine


class DefaultEngine(BaseEngine):
    db = {}

    def __init__(self, _: str, table: str) -> None:
        self.table = table

    def _get(self, resource_id: UUID) -> dict:
        try:
            return self.db[resource_id]
        except KeyError as exception:
            raise self.exception(
                self.status.HTTP_404_NOT_FOUND, "not found") from exception

    async def db_insert_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self.db[resource_id] = resource_obj
        return {"id": resource_id, **resource_obj}

    async def db_select_one(self, resource_id: UUID) -> dict:
        return {"id": resource_id, **self._get(resource_id)}

    async def db_update_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self._get(resource_id)
        self.db[resource_id] = resource_obj
        return {"id": resource_id, **resource_obj}

    async def db_delete_one(self, resource_id: UUID) -> None:
        self._get(resource_id)
        self.db.pop(resource_id, None)
        return None

    async def db_select_all(self, skip: NonNegativeInt = 0, limit: NonNegativeInt = 100) -> list[dict]:
        return [{"id": k, **v} for k, v in self.db.items()][skip:limit]
