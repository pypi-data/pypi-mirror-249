# Forager service

A python wrapper for the Hunter.io v2 api with additinal crud service.

## Installation

### Requirements

    - Python 3.10
    - httpx

### To install

   pip install forager_service==0.1.1

## Usage

Service supports next method from Hunter.io v2 api

    - domain_search (with async adomain_search)
    - email_finder (with async aemail_finder)
    - verify_email (with async averify_email)
    - email_count (with async aemail_count)
    
Additionally, service supports crud methods for locally storing data

## How to use service

### Import service and instantiate it once

    from forager_service.hunter import HunterService

    initializer = HunterService()

    initializer.initialize_service("api_key_got_from_hunter")

    initializer.initialize_async_service("api_key_got_from_hunter")

    hunter = initializer.service 

    async_hunter = initializer.async_service


### Once initialized somewhere in the code you can get instances in different places without additional initialization

    hunter = HunterService().service

    async_hunter = HunterService().async_service

### All data stores in crud_service internal storage.

### Search addresses for a given domain

    hunter.domain_search("www.brillion.com.ua")

### Or pass company name

    hunter.domain_search(company="Brillion", limit=20, seniority="junior")

### Find email address

    hunter.email_finder(compayny="pmr", full_name="Sergiy Petrov", raw=True)

### Check email deliverabelity

    hunter.email_verifier("a@a.com")

### CRUD operations can be performed to manipulate received data

    from forager_service.app_services.crud_service import CRUDService

    crud_service = CRUDService()

    crud_service.create("company_email", hunter.domain_search("company.com.ua"))

### To collect email validation and other info use email_verify_record_handler. Data will be saved in local storage.

    from forager_service.operation_handlers.email_verify_record_handler import EmailVerifyCRUDHandler

    email_handler = EmailVerifyCRUDHandler()

    email_handler.create_email_record("some_email@company.com")

    email_handler.read("another@company.com")

## Tests

    To run test firstly you need to install test dependency, then run

        pytest -cov
