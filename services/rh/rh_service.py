"""Serviço do módulo RH."""

from __future__ import annotations

from infraesctruture.auth.authorization import requires_resource
from infraesctruture.auth.utils.handler import AccessDeniedError

from domain.rh.extras import Extras
from repositories.rh.rh_repository import RHRepository
from services.base_service import Service, ServiceResponse
from shared.records import Records


class RHService(Service):

    def __init__(self):

        repository = RHRepository()

        super().__init__(

            domain={
                "extras": Extras(repository=repository),
            },

            repository=repository,

        )

    def allowed(
        self,
        forms,
        records: Records | None = None,
        *,
        resources: set[int] | None = None,
        authenticated: bool = False,
    ):

        return forms.by_keys(

            "extras",

            resources=resources,

            authenticated=authenticated,

        )

    def process(
        self,
        key: str,
        records: Records,
    ) -> ServiceResponse:

        if key not in ('extras',):
            raise AccessDeniedError()

        return getattr(

            self,
            key,

        )(

            records,

        )

    @requires_resource('rh', 'extras')
    def extras(
        self,
        records: Records,
    ) -> ServiceResponse:

        domain = self.domain["extras"]

        records = domain.identificar(records)

        total = domain.registrar(records)

        return ServiceResponse(

            key="extras",

            data={
                "records": records,
                "total": total,
            },

        )
