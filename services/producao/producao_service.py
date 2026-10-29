"""Serviços do módulo Produção."""

from __future__ import annotations

from infraesctruture.auth.authorization import requires_resource
from infraesctruture.auth.utils.handler import AccessDeniedError

from domain.producao.producao import Producao

from repositories.producao.producao_repository import (
    ProducaoRepository,
)

from services.base_service import Service

from shared.records import Records


class ProducaoService(Service):

    def __init__(
        self,
    ):

        repository = ProducaoRepository()

        super().__init__(

            repository=repository,

            domain={

                "ensaques": Producao(
                    repository=repository,
                ),

                "paradas": Producao(
                    repository=repository,
                ),

                "output": Producao(
                    repository=repository,
                ),

            },

        )

    # ==========================================================
    # MODULE
    # ==========================================================

    def allowed(
        self,
        forms,
        records: Records | None = None,
        *,
        resources: set[int] | None = None,
        authenticated: bool = False,
    ):

        return forms.by_keys(

            "ensaques",
            "paradas",
            "output",

            resources=resources,

            authenticated=authenticated,

        )

    def process(
        self,
        key: str,
        records: Records,
    ) -> Records:

        if key not in ('ensaques', 'paradas', 'output'):
            raise AccessDeniedError()

        return getattr(

            self,

            key,

        )(

            records,

        )

    # ==========================================================
    # ACTIONS
    # ==========================================================

    @requires_resource('production', 'packing')
    def ensaques(
        self,
        records: Records,
    ) -> Records:

        domain = self.domain["ensaques"]

        records = domain.identificar(

            records,

        )

        domain.registrar_ensaques(

            records,

        )

        return records

    @requires_resource('production', 'downtime')
    def paradas(
        self,
        records: Records,
    ) -> Records:

        domain = self.domain["paradas"]

        domain.registrar_paradas(
            records,
        )

        return records

    @requires_resource('production', 'production')
    def output(
        self,
        records: Records,
    ) -> Records:

        domain = self.domain["output"]

        records = domain.identificar(

            records,

        )

        domain.registrar_producao(

            records,

        )

        return records
