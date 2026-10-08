"""Tela de entrada e Home autenticada."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.app.registry import ModuleRegistration


@dataclass(frozen=True, slots=True)
class HomeAction:
    key: str
    email: str = ""
    password: str = ""
    confirmation: str = ""


class HomeModule:
    """Renderiza autenticação e a página inicial após o login."""

    def respond(
        self,
        *,
        authenticated: bool,
        step: str,
        email: str,
        error: str | None,
        username: str | None,
        modules: tuple[ModuleRegistration, ...],
    ) -> HomeAction | str | None:
        if not authenticated:
            return self._authentication(step, email, error)

        st.title("📥 Cadastra.me")
        st.subheader(f"Bem-vindo, {username or 'usuário'}!")
        st.write("Selecione um módulo para começar.")

        available = tuple(module for module in modules if module.definition.key != "home")
        if not available:
            st.info("Seu perfil ainda não possui módulos liberados.")
            return None

        columns = st.columns(len(available))
        for column, module in zip(columns, available):
            with column:
                if st.button(module.label, key=f"home:{module.definition.key}", use_container_width=True):
                    return module.definition.key
        return None

    @staticmethod
    def _authentication(
        step: str,
        email: str,
        error: str | None,
    ) -> HomeAction | None:
        st.title("📥 Cadastra.me")

        if error:
            st.error(error)

        if step == "password":
            st.subheader("Entrar")
            st.caption(f"E-mail: {email}")
            with st.form("authentication-password", clear_on_submit=True):
                password = st.text_input("Senha", type="password")
                submitted = st.form_submit_button("Entrar", use_container_width=True)
            if submitted:
                return HomeAction("login", email=email, password=password)
            if st.button("Usar outro e-mail"):
                return HomeAction("back_to_identify")
            return None

        if step == "create_password":
            st.subheader("Criar senha")
            st.caption(f"Primeiro acesso para: {email}")
            with st.form("authentication-create-password", clear_on_submit=True):
                password = st.text_input("Nova senha", type="password")
                confirmation = st.text_input("Confirmar senha", type="password")
                submitted = st.form_submit_button("Criar senha", use_container_width=True)
            if submitted:
                return HomeAction(
                    "create_password",
                    email=email,
                    password=password,
                    confirmation=confirmation,
                )
            if st.button("Usar outro e-mail"):
                return HomeAction("back_to_identify")
            return None

        st.subheader("Entrar")
        with st.form("authentication-identify"):
            submitted_email = st.text_input(
                "E-mail",
                value=email,
                placeholder="usuario@empresa.com",
            )
            submitted = st.form_submit_button("Continuar", use_container_width=True)
        if submitted:
            return HomeAction("identify", email=submitted_email)
        return None
