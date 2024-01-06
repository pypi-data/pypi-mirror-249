# Forager service

A python wrapper for the Hunter.io v2 api with additinal crud service.

## Installation

### Requirements

    - Python 3.10
    - httpx

### To install

   pip install foreger_service

## Usage

Service supports next method from Hunter.io v2 api

    - domain_search (with async adomain_search)
    - email_finder (with async aemail_finder)
    - verify_email (with async averify_email)
    - email_count (with async aemail_count)
    
Additionally, service supports crud methods for locally storing data

## How to use service

### Import service and instantiate it once

    from config import HunterService

    initializer = HunterService()

    initializer.initialize_service("api_key_got_from_hunter")

    hunter = initializer.get_service()

    crud_service = initializer.get_crud_service()

### Once initialized somewhere in the code you can get instances in different places without additional initialization

    hunter = HunterService().get_service()

    crud_service = HunterService().get_crud_service()

### All data stores in crud_service internal storage.

### Search addresses for a given domain

    hunter.domain_search("www.brillion.com.ua")

### Or pass company name

    hunter.domain_search(company="Brillion", limit=20, seniority="junior")

### Find email address

    hunter.email_finder("pmr", full_name="Sergiy Petrov", raw=True)

### Check email deliverabelity

    hunter.email_verifier("a@a.com")

### CRUD operations can be performed to manipulate received data

    crud_service = HunterService().get_service()

    crud_service.create("company_email", hunter.domain_search("company.com.ua"))

## Tests

    To run test firstly you need to install test dependency, then run

        pytest --cov
