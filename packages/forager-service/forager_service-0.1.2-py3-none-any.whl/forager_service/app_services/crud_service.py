"""CRUD service for Forager project."""
from __future__ import annotations

from typing import Any

from forager_service.common.exceptions import ForagerKeyError
from forager_service.common.validators import common_validators


class CRUDService(object):
    """Service for perform CRUD operations with storage."""

    _storage: dict = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> CRUDService:
        """Create new instance, if it's None, otherwise use earlier created one."""
        if getattr(cls, 'instance', None) is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    @property
    def storage(self) -> dict:
        """Get local storage."""
        return self._storage

    def create(self, key: str, some_data: Any) -> None:
        """Save arbitrary some_data to storage."""
        common_validators.validate_str('storage_key', key)
        if key in self._storage:
            raise ForagerKeyError(
                'Key {key} already presents in storage. Use "update" to modify some_data.'.format(key=key),
            )
        self._storage[key] = some_data

    def read(self, key: str) -> Any:
        """Read value from storage by key."""
        common_validators.validate_str('storage_key', key)
        return self._storage.get(key)

    def update(self, key: str, some_data: Any) -> None:
        """Update key some_data."""
        common_validators.validate_str('storage_key', key)
        if key not in self._storage:
            raise ForagerKeyError(
                'key {key} is not in storage. Use "create" operation.'.format(key=key),
            )
        self._storage[key] = some_data

    def delete(self, key: str) -> Any:
        """Delete key some_data pair and return some_data."""
        common_validators.validate_str('storage_key', key)
        return self._storage.pop(key, None)
