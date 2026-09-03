"""Gerenciamento das configurações de conexão."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Union


class ConnectionType(Enum):
    DATABASE = "databases"
    REPOSITORY = "repositories"
    API = "apis"


class Connection(Enum):
    DW = "warehouse"
    TST = "teste"

    NFES = "nfes"

    METEO = "openmeteo"


# ==========================
# CONFIGS
# ==========================

@dataclass(frozen=True)
class DBConfig:
    name: str
    engine: str

    host: str
    port: int
    database: str

    user: str
    password: str


@dataclass(frozen=True)
class RepoConfig:
    name: str
    engine: str

    share: str
    path: str
    url: str

    user: str
    password: str


@dataclass(frozen=True)
class APIConfig:
    name: str
    engine: str

    base_url: str

    authentication: dict
    configuration: dict


ConfigType = Union[
    DBConfig,
    RepoConfig,
    APIConfig,
]

# ==========================
# SETTINGS
# ==========================

@dataclass(frozen=True)
class ApplicationSettings:
    name: str
    environment: str
    debug: bool
    timezone: str


@dataclass(frozen=True)
class DatabaseSettings:
    default: Connection


@dataclass(frozen=True)
class APISettings:
    default: Connection


@dataclass(frozen=True)
class RepositorySettings:
    default: Connection

# ==========================
# LOADER
# ==========================

@lru_cache
def _load_secrets() -> dict:

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "configs",
        "secrets.json",
    )

    with open(path, encoding="utf-8") as f:
        return json.load(f)

@lru_cache
def _load_settings() -> dict:

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "configs",
        "settings.json",
    )

    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ==========================
# CONFIG
# ==========================

class Config:

    @staticmethod
    def get(
        connection_type: ConnectionType,
        connection: Connection,
    ) -> ConfigType:

        section = _load_secrets().get(
            connection_type.value,
            {}
        )

        cfg = section.get(connection.value)

        if cfg is None:
            raise ValueError(
                f"{connection.value} não encontrado em {connection_type.value}"
            )

        if connection_type is ConnectionType.DATABASE:

            return DBConfig(
                name=connection.value,
                engine=cfg["engine"],
                host=cfg["host"],
                port=cfg["port"],
                database=cfg["database"],
                user=cfg["user"],
                password=cfg["password"],
            )

        if connection_type is ConnectionType.REPOSITORY:

            return RepoConfig(
                name=connection.value,
                engine=cfg["engine"],
                share=cfg["share"],
                path=cfg["path"],
                url=cfg["url"],
                user=cfg["user"],
                password=cfg["password"],
            )

        if connection_type is ConnectionType.API:

            return APIConfig(
                name=connection.value,
                engine=cfg["engine"],
                base_url=cfg["base_url"],
                authentication=cfg["authentication"],
                configuration=cfg["configuration"],
            )

        raise NotImplementedError(
            f"Tipo '{connection_type.value}' não suportado."
        )
    
# ==========================
# SETTINGS
# ==========================

class Settings:

    def __init__(self):

        settings = _load_settings()

        application = settings["application"]
        environment = application["environment"]

        self.application = ApplicationSettings(
            name=application["name"],
            environment=environment,
            debug=application["debug"],
            timezone=application["timezone"],
        )

        self.database = DatabaseSettings(
            default=Connection(
                settings["database"]["connections"][environment]
            )
        )

        self.api = APISettings(
            default=Connection(
                settings["api"]["connections"][environment]
            )
        )

        self.repository = RepositorySettings(
            default=Connection(
                settings["repository"]["connections"][environment]
            )
        )