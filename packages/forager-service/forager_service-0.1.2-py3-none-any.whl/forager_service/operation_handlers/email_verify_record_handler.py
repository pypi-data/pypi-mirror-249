"""Handler for verified email records CRUD operations."""
from typing import Optional

import httpx

from forager_service.app_services.crud_service import CRUDService
from forager_service.app_services.service import Service
from forager_service.hunter import HunterService


class EmailVerifyCRUDHandler(object):
    """Class for process email verification state info."""

    _crud_service: CRUDService = CRUDService()
    _hunter: Optional[Service] = None

    def __init__(self) -> None:
        """Initialize class instance."""
        hunter_service = HunterService()
        self._hunter = hunter_service.service

    def create_email_record(self, email: str) -> Optional[bool]:
        """
        Create email record in storage.

        :param email: str Email to create record.
        :return: bool True, if operation was successfull, otherwise False. If email in storage - None.
        """
        if self._crud_service.storage.get(email) or self._hunter is None:
            return None
        received_data: dict | httpx.Response = self._hunter.verify_email(email)
        if not isinstance(received_data, dict):
            return None
        if received_data.get('errors') is not None:
            return False
        self._crud_service.create(
            email,
            {
                'status': received_data.get('status'),
                'result': received_data.get('result'),
                'sources': received_data.get('sources'),
            },
        )
        return True

    def read_email_record(self, email: str) -> Optional[dict]:
        """
        Read email record from storage.

        :param email: str Email to retrieve.
        :return: dict Email info or None.
        """
        return self._crud_service.read(email)

    def update_email_record(self, email: str, param_dict: dict) -> bool:
        """
        Update email record in storage.

        :param email: str Email to update.
        :param param_dict: dict Data to update.
        :return: True, if email data updated, otherwise - False.
        """
        if self._crud_service.storage.get(email, None) is None:
            return False
        self._crud_service.update(email, param_dict)
        return True

    def delete_email_record(self, email: str) -> None:
        """
        Delete email record from storage.

        :param email: str Email to delete.
        :return: None
        """
        self._crud_service.delete(email)
