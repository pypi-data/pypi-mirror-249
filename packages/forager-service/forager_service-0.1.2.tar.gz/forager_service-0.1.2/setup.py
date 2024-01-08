# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forager_service',
 'forager_service.app_services',
 'forager_service.common',
 'forager_service.operation_handlers']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.26.0,<0.27.0']

setup_kwargs = {
    'name': 'forager-service',
    'version': '0.1.2',
    'description': 'Hunter.io v2 api implementation',
    'long_description': '# Forager service\n\nA python wrapper for the Hunter.io v2 api with additinal crud service.\n\n## Installation\n\n### Requirements\n\n    - Python 3.10\n    - httpx\n\n### To install\n\n   pip install forager_service==0.1.1\n\n## Usage\n\nService supports next method from Hunter.io v2 api\n\n    - domain_search (with async adomain_search)\n    - email_finder (with async aemail_finder)\n    - verify_email (with async averify_email)\n    - email_count (with async aemail_count)\n    \nAdditionally, service supports crud methods for locally storing data\n\n## How to use service\n\n### Import service and instantiate it once\n\n    from forager_service.hunter import HunterService\n\n    initializer = HunterService()\n\n    initializer.initialize_service("api_key_got_from_hunter")\n\n    initializer.initialize_async_service("api_key_got_from_hunter")\n\n    hunter = initializer.service \n\n    async_hunter = initializer.async_service\n\n\n### Once initialized somewhere in the code you can get instances in different places without additional initialization\n\n    hunter = HunterService().service\n\n    async_hunter = HunterService().async_service\n\n### All data stores in crud_service internal storage.\n\n### Search addresses for a given domain\n\n    hunter.domain_search("www.brillion.com.ua")\n\n### Or pass company name\n\n    hunter.domain_search(company="Brillion", limit=20, seniority="junior")\n\n### Find email address\n\n    hunter.email_finder(compayny="pmr", full_name="Sergiy Petrov", raw=True)\n\n### Check email deliverabelity\n\n    hunter.email_verifier("a@a.com")\n\n### CRUD operations can be performed to manipulate received data\n\n    from forager_service.app_services.crud_service import CRUDService\n\n    crud_service = CRUDService()\n\n    crud_service.create("company_email", hunter.domain_search("company.com.ua"))\n\n### To collect email validation and other info use email_verify_record_handler. Data will be saved in local storage.\n\n    from forager_service.operation_handlers.email_verify_record_handler import EmailVerifyCRUDHandler\n\n    email_handler = EmailVerifyCRUDHandler()\n\n    email_handler.create_email_record("some_email@company.com")\n\n    email_handler.read("another@company.com")\n\n## Tests\n\n    To run test firstly you need to install test dependency, then run\n\n        pytest -cov\n',
    'author': 'victro-nuzhniy',
    'author_email': 'nuzhniyva@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/victor-nuzhniy/forager.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
