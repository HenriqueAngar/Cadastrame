"""Classe base para módulos da aplicação."""

from __future__ import annotations

from dataclasses import dataclass, field

import streamlit as st

from ui.components.modules.assets import AssetRegistry
from ui.components.modules.navigator import FormNavigator


@dataclass(frozen=True, slots=True)
class ModuleDefinition:
    """Metadados declarativos de um módulo."""

    key: str
    title: str
    icon: str
    navigator: bool = True
    resource_page_code: str | None = None
    placeholder: str = "Aqui haverá formulários deste módulo."


@dataclass(slots=True)
class Module:
    """Base para módulos; mantém assets preparados para a próxima etapa."""

    definition: ModuleDefinition
    assets: AssetRegistry
    navigator: FormNavigator = field(init=False)

    def __post_init__(self) -> None:
        self.navigator = FormNavigator(self.definition.key)

    def respond(self) -> None:
        st.title(f"{self.definition.icon} {self.definition.title}")
        st.info(self.definition.placeholder)
        return None
