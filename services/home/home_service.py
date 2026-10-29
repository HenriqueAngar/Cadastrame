"""Serviços de autenticação."""

from __future__ import annotations

from domain.home.login import Login
from domain.home.password import Password

from services.base_service import Service

from shared.records import Records


class HomeService(Service):

    def __init__(self):

        super().__init__(

            domain={

                "login": Login,

                "password": Password,

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

        step = "login"

        if records is not None:

            step = records.metadata.get(

                "step",

                "login",

            )

        return forms.by_keys(

            step,

            resources=resources,

            authenticated=authenticated,

        )

    def process(
        self,
        key: str,
        records: Records,
    ) -> Records:

        return getattr(

            self,

            key,

        )(

            records,

        )

    # ==========================================================
    # DOMAIN
    # ==========================================================

    def login(
        self,
        records: Records,
    ) -> Records:

        record = records.data[0]

        response = Records()

        response.metadata["key"] = "identify"

        response.add(

            self.domain["login"](

                email=record["email"],

            )

        )

        return response

    def password(
        self,
        records: Records,
    ) -> Records:

        record = records.data[0]

        response = Records()

        response.metadata["key"] = "login"

        response.add(

            self.domain["password"](

                email=record["email"],

                value=record["password"],

            )

        )

        return response

    def create_password(
        self,
        records: Records,
    ) -> Records:

        record = records.data[0]

        response = Records()

        response.metadata["key"] = "create_password"

        response.add(

            self.domain["password"](

                email=record["email"],

                value=record["password"],

                confirmation=record["confirmation"],

            )

        )

        return response
