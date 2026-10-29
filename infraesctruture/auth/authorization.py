"""Autorização obrigatória nas operações dos serviços."""
from functools import wraps
from infraesctruture.auth.manager import AuthManager


def requires_resource(page_code: str, form_code: str):
    def decorate(function):
        @wraps(function)
        def authorized(*args, **kwargs):
            AuthManager().require_resource(page_code, form_code)
            return function(*args, **kwargs)
        return authorized
    return decorate
