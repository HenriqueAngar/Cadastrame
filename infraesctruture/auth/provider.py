"""Provedor de acesso aos dados de autenticação."""

from __future__ import annotations

from infraesctruture.connection.manager import manager

from infraesctruture.auth.utils.models import (
    Resource,
    UserRecord,
)
from infraesctruture.auth.utils import queries


class AuthProvider:

    # ==========================================================
    # SELECT
    # ==========================================================

    @staticmethod
    def get_user_by_email(
        email: str,
    ) -> UserRecord | None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.GET_USER_BY_EMAIL,
                    (email,),
                )

                row = cur.fetchone()

                if row is None:
                    return None

                return UserRecord(*row)

    @staticmethod
    def get_role_resources(
        idrole: int,
    ) -> list[Resource]:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.GET_ROLE_RESOURCES,
                    (idrole,),
                )

                rows = cur.fetchall()

                return [
                    Resource(*row)
                    for row in rows
                ]

    # ==========================================================
    # UPDATE
    # ==========================================================

    @staticmethod
    def update_password(
        iduser: int,
        password: str,
    ) -> None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.UPDATE_PASSWORD,
                    (
                        password,
                        iduser,
                    ),
                )

    @staticmethod
    def update_last_login(
        iduser: int,
    ) -> None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.UPDATE_LAST_LOGIN,
                    (iduser,),
                )

    @staticmethod
    def activate_user(
        iduser: int,
    ) -> None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.ACTIVATE_USER,
                    (iduser,),
                )

    @staticmethod
    def deactivate_user(
        iduser: int,
    ) -> None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.DEACTIVATE_USER,
                    (iduser,),
                )

    @staticmethod
    def update_email(
        iduser: int,
        email: str,
    ) -> None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.UPDATE_EMAIL,
                    (
                        email,
                        iduser,
                    ),
                )

    @staticmethod
    def update_username(
        iduser: int,
        username: str,
    ) -> None:

        with manager.database() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    queries.UPDATE_USERNAME,
                    (
                        username,
                        iduser,
                    ),
                )