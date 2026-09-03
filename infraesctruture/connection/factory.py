"""Factory responsável pela criação das conexões."""

from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

from psycopg_pool import ConnectionPool
import requests

from infraesctruture.connection.config import (
    APIConfig,
    Config,
    Connection,
    ConnectionType,
    DBConfig,
    RepoConfig,
)
from infraesctruture.connection.policy import (
    APIPolicy,
    DBPolicy,
    RepoPolicy,
)


Policy: TypeAlias = DBPolicy | APIPolicy | RepoPolicy | None


class ConnectionFactory:
    """
    Factory responsável por criar conexões com recursos externos.
    """

    @staticmethod
    def create(
        connection_type: ConnectionType,
        connection: Connection,
        policy: Policy = None,
    ):

        match connection_type:

            case ConnectionType.DATABASE:
                return ConnectionFactory._create_database(
                    connection,
                    policy,
                )

            case ConnectionType.REPOSITORY:
                return ConnectionFactory._create_repository(
                    connection,
                    policy,
                )

            case ConnectionType.API:
                return ConnectionFactory._create_api(
                    connection,
                    policy,
                )

        raise NotImplementedError(
            f"Tipo '{connection_type.value}' não suportado."
        )

    # ==========================================================
    # DATABASE
    # ==========================================================

    @staticmethod
    def _create_database(
        connection: Connection,
        policy: Policy,
    ) -> ConnectionPool:

        cfg: DBConfig = Config.get(
            ConnectionType.DATABASE,
            connection,
        )

        if policy is None:
            policy = DBPolicy()

        conninfo = (
            f"host={cfg.host} "
            f"port={cfg.port} "
            f"dbname={cfg.database} "
            f"user={cfg.user} "
            f"password={cfg.password} "
            f"connect_timeout={policy.connect_timeout}"
        )

        kwargs = {}

        if policy.statement_timeout_ms is not None:

            kwargs["options"] = (
                f"-c statement_timeout={policy.statement_timeout_ms}"
            )

        return ConnectionPool(
            conninfo=conninfo,
            kwargs=kwargs,
            min_size=1,
            max_size=10,
            timeout=30,
            open=True,
        )

    # ==========================================================
    # REPOSITORY
    # ==========================================================

    @staticmethod
    def _create_repository(
        connection: Connection,
        policy: Policy,
    ) -> RepoConfig:

        cfg: RepoConfig = Config.get(
            ConnectionType.REPOSITORY,
            connection,
        )

        repository = Path(cfg.share) / cfg.path

        if not repository.exists():
            raise FileNotFoundError(
                f"Repositório '{repository}' não encontrado."
            )

        return cfg

    # ==========================================================
    # API
    # ==========================================================

    @staticmethod
    def _create_api(
        connection: Connection,
        policy: Policy,
    ) -> requests.Session:

        cfg: APIConfig = Config.get(
            ConnectionType.API,
            connection,
        )

        session = requests.Session()

        auth = cfg.authentication or {}

        auth_type = auth.get(
            "type",
            "none",
        ).lower()

        match auth_type:

            case "none":
                pass

            case "basic":

                params = auth.get(
                    "parameters",
                    {},
                )

                session.auth = (
                    params["user"],
                    params["password"],
                )

            case "bearer":

                params = auth.get(
                    "parameters",
                    {},
                )

                session.headers.update(
                    {
                        "Authorization": f"Bearer {params['token']}"
                    }
                )

            case _:

                raise NotImplementedError(
                    f"Autenticação '{auth_type}' não suportada."
                )

        configuration = cfg.configuration or {}

        headers = configuration.get(
            "headers",
            {},
        )

        if headers:
            session.headers.update(headers)

        # Guarda a configuração para uso futuro
        session.connection_config = cfg
        session.connection_policy = policy

        return session