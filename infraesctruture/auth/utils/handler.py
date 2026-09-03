"""Tratamento dos erros da autenticação."""

from __future__ import annotations

from enum import Enum


# ==========================================================
# AUTHENTICATION STATUS
# ==========================================================

class AuthenticationStatus(Enum):

    USER_NOT_FOUND = "user_not_found"

    PASSWORD_REQUIRED = "password_required"
    
    FIRST_ACCESS = "first_access"
    
    AUTHENTICATED = "authenticated"


# ==========================================================
# EXCEPTIONS
# ==========================================================

class AuthenticationError(Exception):
    """Erro base da autenticação."""


class UserNotFoundError(AuthenticationError):
    """Usuário não encontrado."""


class InvalidPasswordError(AuthenticationError):
    """Senha inválida."""


class InactiveUserError(AuthenticationError):
    """Usuário desativado."""


# ==========================================================
# MESSAGES
# ==========================================================

_MESSAGES = {

    UserNotFoundError:
        "Usuário não encontrado.",

    InvalidPasswordError:
        "Senha inválida.",

    InactiveUserError:
        "Usuário desativado.",

}


def message(
    exception: Exception,
) -> str:
    """
    Retorna uma mensagem amigável para erros de autenticação.
    """

    return _MESSAGES.get(
        type(exception),
        "Ocorreu um erro inesperado."
    )


def is_authentication_error(
    exception: Exception,
) -> bool:
    """
    Verifica se a exceção pertence ao domínio da autenticação.
    """

    return isinstance(
        exception,
        AuthenticationError,
    )

