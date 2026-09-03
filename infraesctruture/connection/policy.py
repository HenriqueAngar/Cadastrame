"""Políticas de conexão."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DBPolicy:
    """
    Política de conexão para bancos de dados.
    """

    # Tempo máximo para estabelecer conexão.
    connect_timeout: int = 5

    # Tempo máximo permitido para execução de uma instrução SQL.
    statement_timeout_ms: int | None = None

    # Define se cada comando será confirmado automaticamente.
    autocommit: bool = False


@dataclass(frozen=True)
class APIPolicy:
    """
    Política de comunicação com APIs.
    """

    pass


@dataclass(frozen=True)
class RepoPolicy:
    """
    Política de acesso a repositórios de arquivos.
    """

    pass