"""Orquestração do fluxo de navegação da aplicação."""

from __future__ import annotations

import streamlit as st

from ui.app.navigator import Navigator
from ui.app.registry import ModuleRegistry


class Navigation:
    """Controla o shell da aplicação e a troca entre módulos."""

    def __init__(self) -> None:
        self._navigator = Navigator()
        self._registry = ModuleRegistry()

    def run(self) -> None:
        """Renderiza o módulo atual e a navegação compartilhada."""

        registrations = self._registry.all()

        selected_label = st.sidebar.radio(
            "Navegação",
            [registration.label for registration in registrations],
            index=self._registry.index(self._navigator.module),
        )

        selected = next(
            registration
            for registration in registrations
            if registration.label == selected_label
        )

        if self._navigator.open_module(selected.definition.key):
            st.rerun()

        st.sidebar.divider()
        st.sidebar.caption("Fundação UI/UX — protótipo arquitetural")

        component = selected.module()
        response = component.respond()

        if isinstance(response, str):
            self._navigator.open_module(response)
            st.rerun()

