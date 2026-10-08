"""Estado de autenticação e navegação da aplicação."""

from __future__ import annotations

import streamlit as st


class Navigator:
    """Mantém o estado transitório entre reruns do Streamlit."""

    def __init__(self) -> None:
        st.session_state.setdefault("application_module", "home")
        st.session_state.setdefault("authentication_step", "identify")
        st.session_state.setdefault("authentication_email", "")
        st.session_state.setdefault("authentication_error", None)

    @property
    def module(self) -> str:
        return st.session_state.application_module

    @property
    def authentication_step(self) -> str:
        return st.session_state.authentication_step

    @property
    def email(self) -> str:
        return st.session_state.authentication_email

    @property
    def error(self) -> str | None:
        return st.session_state.authentication_error

    def open_module(self, module: str) -> bool:
        changed = module != self.module
        st.session_state.application_module = module
        return changed

    def set_authentication(
        self,
        *,
        step: str,
        email: str | None = None,
        error: str | None = None,
    ) -> None:
        st.session_state.authentication_step = step
        if email is not None:
            st.session_state.authentication_email = email
        st.session_state.authentication_error = error

    def reset(self) -> None:
        """Limpa o estado temporário e volta à tela de identificação."""
        st.session_state.application_module = "home"
        st.session_state.authentication_step = "identify"
        st.session_state.authentication_email = ""
        st.session_state.authentication_error = None
