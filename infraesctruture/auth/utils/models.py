from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


# ==========================================================
# USER RECORD
# ==========================================================

@dataclass(slots=True, frozen=True)
class UserRecord:
    """
    Representa um registro completo da tabela cadastrame.users.
    Utilizado exclusivamente pela camada de acesso aos dados.
    """

    iduser: int

    idrole: int

    active: bool

    username: str

    email: str

    password: str | None

    created_at: datetime

    updated_at: datetime

    deactivated_at: datetime


# ==========================================================
# RESOURCES
# ==========================================================

@dataclass(slots=True, frozen=True)
class Resource:
    """
    Recurso disponível na aplicação.
    """

    id: int

    page_code: str

    form_code: str | None

    description: str


# ==========================================================
# USER CONTEXT
# ==========================================================

@dataclass(slots=True, frozen=True)
class UserContext:
    """
    Informações do usuário autenticado.

    Nunca contém informações sensíveis.
    """

    iduser: int

    idrole: int

    username: str

    email: str

    resources: tuple[Resource, ...]