"""Gerenciador central de recursos."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import TypeAlias

from psycopg_pool import ConnectionPool

from infraesctruture.connection.config import (
    Connection,
    ConnectionType,
    Settings,
)
from infraesctruture.connection.factory import ConnectionFactory
from infraesctruture.connection.policy import (
    APIPolicy,
    DBPolicy,
    RepoPolicy,
)

Policy: TypeAlias = DBPolicy | APIPolicy | RepoPolicy | None


class ConnectionManager:

    def __init__(
        self,
        settings: Settings | None = None,
    ):

        self.settings = settings or Settings()

        # Policies registradas por recurso
        self._policies: dict[Connection, Policy] = {}

        # Recursos gerenciados
        self._db_pools: dict[Connection, ConnectionPool] = {}
        self._api_sessions: dict[Connection, object] = {}
        self._repositories: dict[Connection, object] = {}

        # Controle de uso
        self._last_used: dict[Connection, datetime] = {}

        # Recursos inativos por mais de 10 minutos serão encerrados
        self._idle_timeout = timedelta(minutes=10)

    # ==========================================================
    # POLICIES
    # ==========================================================

    def register_policy(
        self,
        connection: Connection,
        policy: Policy,
    ) -> None:

        self._policies[connection] = policy

    def policy(
        self,
        connection: Connection,
    ) -> Policy:

        return self._policies.get(connection)

    # ==========================================================
    # CLEANUP
    # ==========================================================

    def _touch(
        self,
        connection: Connection,
    ) -> None:

        self._last_used[connection] = datetime.now()

    def cleanup(self) -> None:

        now = datetime.now()

        expired = [

            connection

            for connection, last_used in self._last_used.items()

            if now - last_used > self._idle_timeout

        ]

        for connection in expired:

            pool = self._db_pools.pop(
                connection,
                None,
            )

            if pool:
                pool.close()

            session = self._api_sessions.pop(
                connection,
                None,
            )

            if session:
                session.close()

            self._repositories.pop(
                connection,
                None,
            )

            self._last_used.pop(
                connection,
                None,
            )

    # ==========================================================
    # DATABASE
    # ==========================================================

    @contextmanager
    def database(
        self,
        connection: Connection | None = None,
    ):

        connection = (
            connection
            or self.settings.database.default
        )

        self.cleanup()

        pool = self._db_pools.get(connection)

        if pool is None:

            pool = ConnectionFactory.create(
                ConnectionType.DATABASE,
                connection,
                self.policy(connection),
            )

            self._db_pools[connection] = pool

        self._touch(connection)

        with pool.connection() as conn:

            yield conn

    # ==========================================================
    # API
    # ==========================================================

    def api(
        self,
        connection: Connection | None = None,
    ):

        connection = (
            connection
            or self.settings.api.default
        )

        self.cleanup()

        session = self._api_sessions.get(connection)

        if session is None:

            session = ConnectionFactory.create(
                ConnectionType.API,
                connection,
                self.policy(connection),
            )

            self._api_sessions[connection] = session

        self._touch(connection)

        return session

    # ==========================================================
    # REPOSITORY
    # ==========================================================

    def repository(
        self,
        connection: Connection | None = None,
    ):

        connection = (
            connection
            or self.settings.repository.default
        )

        self.cleanup()

        repository = self._repositories.get(connection)

        if repository is None:

            repository = ConnectionFactory.create(
                ConnectionType.REPOSITORY,
                connection,
                self.policy(connection),
            )

            self._repositories[connection] = repository

        self._touch(connection)

        return repository

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self) -> dict:

        now = datetime.now()

        def build(resources: dict):

            result = {}

            for connection in resources:

                last_used = self._last_used.get(connection)

                result[connection.name] = {

                    "status": "ACTIVE",

                    "last_used": (
                        last_used.strftime("%Y-%m-%d %H:%M:%S")
                        if last_used
                        else None
                    ),

                    "idle_seconds": (
                        round((now - last_used).total_seconds())
                        if last_used
                        else None
                    ),

                }

            return result

        return {

            "databases": build(self._db_pools),

            "apis": build(self._api_sessions),

            "repositories": build(self._repositories),

        }

    # ==========================================================
    # SHUTDOWN
    # ==========================================================

    def shutdown(self) -> None:

        for pool in self._db_pools.values():
            pool.close()

        for session in self._api_sessions.values():
            session.close()

        self._db_pools.clear()
        self._api_sessions.clear()
        self._repositories.clear()
        self._policies.clear()
        self._last_used.clear()


manager = ConnectionManager()