"""Classe base para serviços da aplicação."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ==========================================================
# RESPONSE
# ==========================================================

@dataclass(slots=True, frozen=True)
class ServiceResponse:
    """
    Resposta produzida por um serviço.

    O módulo devolve esta resposta ao
    Navigation, que encaminha a ação
    para a infraestrutura.
    """

    key: str

    data: Any


# ==========================================================
# SERVICE
# ==========================================================

@dataclass(slots=True)
class Service:
    """
    Classe base para serviços da aplicação.

    Um serviço coordena:

        • Domain

        • Repository / Infrastructure

    e responde ao módulo através de um
    contrato único.
    """

    domain: Any | None = None

    repository: Any | None = None

    # ==========================================================
    # MODULE
    # ==========================================================

    def allowed(
        self,
        *args,
        **kwargs,
    ):
        """
        Define quais recursos do módulo
        devem ser disponibilizados.
        """

        raise NotImplementedError

    # ==========================================================
    # ACTIONS
    # ==========================================================

    def process(
        self,
        *args,
        **kwargs,
    ) -> ServiceResponse:
        """
        Processa a ação solicitada pelo
        módulo e devolve uma resposta
        padronizada.
        """

        raise NotImplementedError

    def submit(
        self,
        *args,
        **kwargs,
    ) -> ServiceResponse:
        """
        Executa a ação principal do
        serviço.
        """

        raise NotImplementedError