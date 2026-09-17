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


@dataclass(slots=True)
class Module:
    """Base incompleta para módulos orientados a assets."""

    definition: ModuleDefinition
    assets: AssetRegistry
    navigator: FormNavigator = field(init=False)

    def __post_init__(self) -> None:
        self.navigator = FormNavigator(self.definition.key)

    def respond(self) -> None:
        st.title(f"{self.definition.icon} {self.definition.title}")

        if not self.assets.items:
            st.info("Este módulo está reservado para a próxima etapa.")
            return None

        asset = self.navigator.render(self.assets)
        st.divider()
        st.subheader(asset.label)
        st.caption(
            "Estrutura inicial do asset. O caso de uso será implementado "
            "em uma etapa posterior."
        )
        return None

