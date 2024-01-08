"""Configuration module for Forager project."""
from __future__ import annotations

from typing import Any, Optional

from forager_service.app_services.async_service import AsyncService
from forager_service.app_services.service import Service


class HunterService(object):
    """Singlton class for initialized instance."""

    _hunter_service: Optional[Service] = None
    _async_hunter_service: Optional[AsyncService] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> HunterService:
        """Create new instance, if it's None, otherwise use earlier created one."""
        if getattr(cls, 'instance', None) is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def initialize_service(self, api_key: str) -> None:
        """Initialize hunter instance."""
        self._hunter_service = Service(api_key)

    def initialize_async_service(self, api_key: str) -> None:
        """Initialize async hunter instance."""
        self._async_hunter_service = AsyncService(api_key)

    @property
    def service(self) -> Optional[Service]:
        """Get hunter service instance."""
        return self._hunter_service

    @property
    def async_service(self) -> Optional[AsyncService]:
        """Get hunter service instance."""
        return self._async_hunter_service
