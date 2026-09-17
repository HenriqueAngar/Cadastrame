"""Navegação entre assets de um módulo."""

from __future__ import annotations

import streamlit as st

from ui.components.modules.assets import AssetDefinition, AssetRegistry


class FormNavigator:
    """Mantém o asset selecionado usando o estado da sessão."""

    def __init__(self, key: str) -> None:
        self._state_key = f"{key}:asset"

    def render(self, assets: AssetRegistry) -> AssetDefinition:
        if not assets.items:
            raise ValueError("Nenhum asset disponível para navegação.")

        selected = st.session_state.setdefault(
            self._state_key,
            assets.items[0].key,
        )

        columns = st.columns(len(assets.items))
        for column, asset in zip(columns, assets.items):
            if column.button(
                asset.label,
                use_container_width=True,
                type="primary" if asset.key == selected else "secondary",
            ):
                st.session_state[self._state_key] = asset.key
                st.rerun()

        return next(
            asset for asset in assets.items
            if asset.key == st.session_state[self._state_key]
        )

