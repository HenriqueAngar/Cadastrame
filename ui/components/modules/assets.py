"""Registro genérico dos assets de um módulo."""

from __future__ import annotations

from dataclasses import dataclass

from infraesctruture.auth.utils.models import Resource


@dataclass(frozen=True, slots=True)
class AssetDefinition:
    """Contrato mínimo de um asset de interface."""

    key: str
    label: str
    order: int = 0
    form_code: str | None = None


@dataclass(frozen=True, slots=True)
class AssetRegistry:
    """Coleção ordenada de assets, com filtro por recurso autorizado."""

    items: tuple[AssetDefinition, ...] = ()

    def __init__(self, *assets: AssetDefinition) -> None:
        object.__setattr__(
            self,
            "items",
            tuple(sorted(assets, key=lambda asset: asset.order)),
        )

    def allowed(
        self,
        *,
        page_code: str,
        resources: tuple[Resource, ...],
    ) -> tuple[AssetDefinition, ...]:
        page = page_code.strip().casefold()
        page_resources = tuple(
            resource
            for resource in resources
            if resource.page_code.strip().casefold() == page
        )
        page_wide_access = any(not resource.form_code for resource in page_resources)
        allowed_forms = {
            resource.form_code.strip().casefold()
            for resource in page_resources
            if resource.form_code
        }

        return tuple(
            asset
            for asset in self.items
            if page_wide_access
            or (
                asset.form_code is not None
                and asset.form_code.strip().casefold() in allowed_forms
            )
        )
