"""Registro genérico dos assets de um módulo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssetDefinition:
    """Contrato mínimo de um asset de interface."""

    key: str
    label: str
    order: int = 0


@dataclass(frozen=True, slots=True)
class AssetRegistry:
    """Coleção ordenada de assets disponíveis no módulo."""

    items: tuple[AssetDefinition, ...] = ()

    def __init__(self, *assets: AssetDefinition) -> None:
        object.__setattr__(
            self,
            "items",
            tuple(sorted(assets, key=lambda asset: asset.order)),
        )

