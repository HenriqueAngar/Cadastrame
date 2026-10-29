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


class AccessDeniedError(AuthenticationError):
    """Operação não autorizada para o usuário atual."""


class PasswordAlreadySetError(AuthenticationError):
    """Primeiro acesso não pode sobrescrever uma senha existente."""


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
    AccessDeniedError: "Você não tem permissão para realizar esta operação.",
    PasswordAlreadySetError: "Esta conta já possui senha. Utilize o login ou solicite recuperação de acesso.",

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

