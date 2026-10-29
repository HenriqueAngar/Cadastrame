"""Serviços do módulo PCP."""

from __future__ import annotations

from infraesctruture.auth.authorization import requires_resource
from infraesctruture.auth.utils.handler import AccessDeniedError

from domain.pcp.base_precos import BasePrecos

from repositories.pcp.pcp_repository import BasePrecosRepository

from services.base_service import (
    Service,
    ServiceResponse,
)

from shared.records import Records


class BasePrecosService(Service):

    def __init__(self):

        self.repository = BasePrecosRepository()

        super().__init__(

            domain={

                "baseprecos": BasePrecos(

                    repository=self.repository,

                ),

            },

            repository=self.repository,

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

            "baseprecos",

            resources=resources,

            authenticated=authenticated,

        )

    def process(
        self,
        key: str,
        records: Records,
    ) -> ServiceResponse:

        if key not in ('baseprecos',):
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

    @requires_resource('pcp', 'product_cost')
    def baseprecos(
        self,
        records: Records,
    ) -> ServiceResponse:

        domain = self.domain["baseprecos"]

        records = domain.identificar(

            records,

        )

        total = domain.substituir(

            records,

        )

        return ServiceResponse(

            key="baseprecos",

            data={

                "records": records,

                "total": total,

            },

        )
