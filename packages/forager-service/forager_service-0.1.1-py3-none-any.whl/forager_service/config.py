"""Configuration module for Forager project."""
from __future__ import annotations

from typing import Any, Optional

import httpx

from forager_service.exceptions import ForagerAPIError, ForagerKeyError
from forager_service.services import create_and_validate_params
from forager_service.validators import common_validators


class CRUDService(object):
    """Service for perform CRUD operations with storage."""

    _storage: dict = {}

    def __new__(cls, *args, **kwargs) -> CRUDService:
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
                'key {key} alreade presents in storage. Use "create" operation.'.format(key=key),
            )
        self._storage[key] = some_data

    def delete(self, key: str) -> Any:
        """Delete key some_data pair and return some_data."""
        common_validators.validate_str('storage_key', key)
        return self._storage.pop(key, None)


class HunterService(object):
    """Singlton class for initialized instance."""

    _hunter_service: Optional[Service] = None
    _async_hunter_service: Optional[AsyncService] = None
    _crud_service: CRUDService = CRUDService()

    def __new__(cls, *args, **kwargs) -> HunterService:
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
    def service(self) -> Service:
        """Get hunter service instance."""
        return self._hunter_service

    @property
    def async_service(self) -> AsyncService:
        """Get hunter service instance."""
        return self._async_hunter_service

    @property
    def crud_service(self) -> CRUDService:
        """Get CRUDService instance."""
        return self._crud_service


class Service(object):
    """Service for performing api calls."""

    def __init__(self, api_key: str) -> None:
        """Initialize service."""
        self.api_key: str = api_key
        self.endpoint: str = 'https://api.hunter.io/v2/'

    def domain_search(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        raw: bool = False,
        **kwargs,
    ) -> dict:
        """
        Perform domain_research request. Return all found email addresses.

        :param domain: str The domain on which to search for emails. Must be defined if company is not.
        :param company: str The name of the company on which to search for emails. Must be defined if domain is not.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :param kwargs: Any Can be from the list below:
            - limit: int The maximum number of emails to give back. Default is 10.
            - offset: int The number of emails to skip. Default is 0.
            - email_type: str The type of emails to give back. Can be one of 'personal' or 'generic'.
            - seniority: str The seniority level of the owners of emails to give back. Can be 'junior', 'senior',
            'executive' or a combination of them delimited by a comma.
            - department: str The department where the owners of the emails to give back work. Can be 'executive',
            'it', 'finance', 'management', 'sales', 'legal', 'support', 'hr', 'marketing', 'communication' or a
            combination of them delimited by a comma.
            - required_field: str Get only email addresses that have the selected field(s). The possible values
            are 'full_name', 'position', 'phone_number'. Several fields can be selected (comma-delimited).

        :return: Full payload of the query as a dict, with email addresses found.
        """
        operation: str = 'domain-search'
        param_dict: dict = create_and_validate_params(operation, domain=domain, company=company, **kwargs)
        url: str = '{domain}{operation}'.format(domain=self.endpoint, operation=operation)
        param_dict['api_key'] = self.api_key
        return self._perform_request(url, param_dict=param_dict, raw=raw)

    def email_finder(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        raw: bool = False,
        **kwargs,
    ) -> dict:
        """
        Find the most likely email address from a domain name, first and a last name.

        :param domain: str The domain on which to search for emails. Must be defined if company is not.
        :param company: str The name of the company on which to search for emails. Must be defined if domain is not.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :param kwargs: Any Can be from the list below:
            - first_name: str The person's first name. It doesn't need to be in lowercase.
            - last_name: str The person's last name. It doesn't need to be in lowercase.
            - full_name: str The person's full name. Note that you'll get better results by supplying the person's
            first and last name if you can. It doesn't need to be in lowercase.
            - max_duration: int The maximum duration of the request in seconds.
            Setting a longer duration allows us to refine the results and provide more
            accurate data. It must range between 3 and 20. The default is 10.
        :return: Full payload of the query as a dict, with email addresses found.
        """
        operation: str = 'email-finder'
        param_dict: dict = create_and_validate_params(
            operation,
            domain=domain,
            company=company,
            **kwargs,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        param_dict['api_key'] = self.api_key
        return self._perform_request(url, param_dict=param_dict, raw=raw)

    def verify_email(
        self,
        email: str,
        raw: bool = False,
    ) -> dict:
        """
        Verify the deliverability of an email address.

        :param email: str Email to verify.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :return: Full payload of the query as a dict.
        """
        operation: str = 'email-verifier'
        param_dict: dict = create_and_validate_params(
            operation,
            email=email,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        param_dict['api_key'] = self.api_key
        return self._perform_request(url, param_dict=param_dict, raw=raw)

    def email_count(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        email_type: Optional[str] = None,
        raw: bool = False,
    ) -> dict:
        """
        Count emails for domain or company.

        :param domain: str The domain on which to search for emails. Must be defined if company is not.
        :param company: str The name of the company on which to search for emails. Must be defined if domain is not.
        :param email_type: str The type of emails to give back. Can be one of 'personal' or 'generic'.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :return: Full payload of the query as a dict.
        """
        operation: str = 'email-count'
        param_dict: dict = create_and_validate_params(
            operation,
            domain=domain,
            company=company,
            type=email_type,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        return self._perform_request(url, param_dict=param_dict, raw=raw)

    def _perform_request(
        self,
        url: str,
        method: str = 'get',
        raw: bool = False,
        **kwargs,
    ) -> dict | httpx.Response:
        """Perform http request."""
        request = httpx.Request(
            method,
            url,
            params=kwargs.get('param_dict'),
            json=kwargs.get('payload'),
            headers=kwargs.get('headers'),
        )
        with httpx.Client() as client:
            response = client.send(request)
        if raw:
            return response
        some_data: Optional[dict] = response.json().get('data')
        if some_data is not None:
            return some_data
        raise ForagerAPIError(response.json())


class AsyncService(object):
    """Service for performing api calls."""

    def __init__(self, api_key: str) -> None:
        """Initialize service."""
        self.api_key: str = api_key
        self.endpoint: str = 'https://api.hunter.io/v2/'

    async def domain_search(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        raw: bool = False,
        **kwargs,
    ) -> dict:
        """
        Perform domain_research request. Return all found email addresses.

        :param domain: str The domain on which to search for emails. Must be defined if company is not.
        :param company: str The name of the company on which to search for emails. Must be defined if domain is not.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :param kwargs: Any Can be from the list below:
            - limit: int The maximum number of emails to give back. Default is 10.
            - offset: int The number of emails to skip. Default is 0.
            - email_type: str The type of emails to give back. Can be one of 'personal' or 'generic'.
            - seniority: str The seniority level of the owners of emails to give back. Can be 'junior', 'senior',
            'executive' or a combination of them delimited by a comma.
            - department: str The department where the owners of the emails to give back work. Can be 'executive',
            'it', 'finance', 'management', 'sales', 'legal', 'support', 'hr', 'marketing', 'communication' or a
            combination of them delimited by a comma.
            - required_field: str Get only email addresses that have the selected field(s). The possible values
            are 'full_name', 'position', 'phone_number'. Several fields can be selected (comma-delimited).

        :return: Full payload of the query as a dict, with email addresses found.
        """
        operation: str = 'domain-search'
        param_dict: dict = create_and_validate_params(
            operation,
            domain=domain,
            company=company,
            **kwargs,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        param_dict['api_key'] = self.api_key
        return await self._perform_request(url, param_dict=param_dict, raw=raw)

    async def email_finder(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        raw: bool = False,
        **kwargs,
    ) -> dict:
        """
        Find the most likely email address from a domain name, first and a last name.

        :param domain: str The domain on which to search for emails. Must be defined if company is not.
        :param company: str The name of the company on which to search for emails. Must be defined if domain is not.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :param kwargs: Any Can be from the list below:
            - first_name: str The person's first name. It doesn't need to be in lowercase.
            - last_name: str The person's last name. It doesn't need to be in lowercase.
            - full_name: str The person's full name. Note that you'll get better results by supplying the person's
            first and last name if you can. It doesn't need to be in lowercase.
            - max_duration: int The maximum duration of the request in seconds.
            Setting a longer duration allows us to refine the results and provide more
            accurate data. It must range between 3 and 20. The default is 10.
        :return: Full payload of the query as a dict, with email addresses found.
        """
        operation: str = 'email-finder'
        param_dict: dict = create_and_validate_params(
            operation,
            domain=domain,
            company=company,
            **kwargs,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        param_dict['api_key'] = self.api_key
        return await self._perform_request(url, param_dict=param_dict, raw=raw)

    async def verify_email(
        self,
        email: str,
        raw: bool = False,
    ) -> dict:
        """
        Verify the deliverability of an email address.

        :param email: str Email to verify.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :return: Full payload of the query as a dict.
        """
        operation: str = 'email-verifier'
        param_dict: dict = create_and_validate_params(
            operation,
            email=email,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        param_dict['api_key'] = self.api_key
        return await self._perform_request(url, param_dict=param_dict, raw=raw)

    async def email_count(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        email_type: Optional[str] = None,
        raw: bool = False,
    ) -> dict:
        """
        Count emails for domain or company.

        :param domain: str The domain on which to search for emails. Must be defined if company is not.
        :param company: str The name of the company on which to search for emails. Must be defined if domain is not.
        :param email_type: str The type of emails to give back. Can be one of 'personal' or 'generic'.
        :param raw: bool Gives back the entire response instead of just the 'data'.
        :return: Full payload of the query as a dict.
        """
        operation: str = 'email-count'
        param_dict: dict = create_and_validate_params(
            operation,
            domain=domain,
            company=company,
            type=email_type,
        )
        url: str = '{endpoint}{operation}'.format(endpoint=self.endpoint, operation=operation)
        return await self._perform_request(url, param_dict=param_dict, raw=raw)

    async def _perform_request(
        self,
        url: str,
        method: str = 'get',
        raw: bool = False,
        **kwargs,
    ):
        """Perform async http request."""
        request = httpx.Request(
            method,
            url,
            params=kwargs.get('param_dict'),
            json=kwargs.get('payload'),
            headers=kwargs.get('headers'),
        )
        async with httpx.AsyncClient() as client:
            response = await client.send(request)
        if raw:
            return response
        some_data: Optional[dict] = response.json().get('data')
        if some_data is not None:
            return some_data
        raise ForagerAPIError(response.json())
