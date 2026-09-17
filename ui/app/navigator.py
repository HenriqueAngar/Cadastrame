"""Estado mínimo da navegação da aplicação."""

from __future__ import annotations

import streamlit as st


class Navigator:
    """Mantém o módulo selecionado durante a sessão Streamlit."""

    def __init__(self) -> None:
        st.session_state.setdefault("application_module", "home")

    @property
    def module(self) -> str:
        """Retorna a chave do módulo atual."""

        return st.session_state.application_module

    def open_module(self, module: str) -> bool:
        """Seleciona um módulo e informa se houve mudança."""

        changed = module != self.module
        st.session_state.application_module = module
        return changed

    def reset(self) -> None:
        """Retorna o fluxo para a Home."""

        self.open_module("home")

