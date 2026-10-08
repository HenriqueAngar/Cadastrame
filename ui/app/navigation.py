"""Orquestra autenticação, autorização e navegação principal."""

from __future__ import annotations

import logging

import streamlit as st

from infraesctruture.auth.manager import AuthManager
from infraesctruture.auth.utils.handler import (
    AuthenticationError,
    AuthenticationStatus,
    message as authentication_message,
)
from services.home.home_service import HomeService
from ui.app.navigator import Navigator
from ui.app.registry import ModuleRegistration, ModuleRegistry
from ui.modules.home.home_module import HomeAction, HomeModule

logger = logging.getLogger(__name__)


class Navigation:
    """Mantém o usuário na Home até autenticar e filtra áreas por recurso."""

    def __init__(self) -> None:
        self._auth = AuthManager()
        self._home_service = HomeService(self._auth)
        self._navigator = Navigator()
        self._registry = ModuleRegistry()

    def run(self) -> None:
        session = self._auth.session
        authenticated = session.authenticated

        if authenticated and session.expired():
            self._navigator.reset()
            st.rerun()

        authenticated = session.authenticated
        if authenticated:
            session.touch()
            started_at = st.session_state.get("started_at")
            self._navigation_key = (
                f"application-navigation-{started_at.isoformat()}"
                if started_at
                else "application-navigation"
            )
        else:
            self._navigator.reset()

        resources = session.user.resources if authenticated and session.user else ()
        registrations = self._registry.allowed(
            resources,
            authenticated=authenticated,
        )

        if self._navigator.module not in {
            registration.definition.key for registration in registrations
        }:
            self._navigator.open_module("home")

        if authenticated:
            if st.sidebar.button("Sair", key="application-logout", use_container_width=True):
                self._auth.logout()
                self._navigator.reset()
                st.rerun()
            selected = self._select_module(registrations)
        else:
            selected = self._registry.by_key("home")

        if self._navigator.module != selected.definition.key:
            self._navigator.open_module(selected.definition.key)
            st.rerun()

        if selected.definition.key == "home":
            response = HomeModule().respond(
                authenticated=authenticated,
                step=self._navigator.authentication_step,
                email=self._navigator.email,
                error=self._navigator.error,
                username=session.user.username if authenticated and session.user else None,
                modules=registrations,
            )
            self._handle_home_response(response, registrations)
            return

        selected.module().respond()

    def _select_module(
        self,
        registrations: tuple[ModuleRegistration, ...],
    ) -> ModuleRegistration:
        home = self._registry.by_key("home")
        if self._navigator.module == "home":
            return home

        if st.sidebar.button("Home", key="application-home"):
            return home

        available = tuple(
            registration
            for registration in registrations
            if registration.definition.key != "home"
        )
        if not available:
            return home

        labels = [registration.label for registration in available]
        selected_label = st.sidebar.radio(
            "Navegação",
            labels,
            index=self._registry.index(self._navigator.module, available),
            key=self._navigation_key,
        )
        return next(registration for registration in available if registration.label == selected_label)

    def _handle_home_response(
        self,
        response: HomeAction | str | None,
        registrations: tuple[ModuleRegistration, ...],
    ) -> None:
        if isinstance(response, str):
            selected = next(
                (
                    registration
                    for registration in registrations
                    if registration.definition.key == response
                ),
                None,
            )
            if selected is not None:
                # The sidebar radio is not rendered on Home, so its next
                # selection can safely follow the Home shortcut.
                if self._auth.session.authenticated:
                    st.session_state[self._navigation_key] = selected.label
                self._navigator.open_module(response)
                st.rerun()
            return

        if not isinstance(response, HomeAction):
            return

        if response.key == "back_to_identify":
            self._navigator.set_authentication(step="identify", email="")
            st.rerun()

        try:
            if response.key == "identify":
                status = self._home_service.identify(response.email)
                if status is AuthenticationStatus.USER_NOT_FOUND:
                    self._navigator.set_authentication(
                        step="identify",
                        email=response.email.strip(),
                        error="Este e-mail não possui acesso ao Cadastrame.",
                    )
                elif status is AuthenticationStatus.FIRST_ACCESS:
                    self._navigator.set_authentication(
                        step="create_password",
                        email=response.email.strip().lower(),
                    )
                elif status is AuthenticationStatus.PASSWORD_REQUIRED:
                    self._navigator.set_authentication(
                        step="password",
                        email=response.email.strip().lower(),
                    )
            elif response.key == "login":
                self._home_service.authenticate(response.email, response.password)
                self._authenticated_home()
            elif response.key == "create_password":
                self._home_service.create_password(
                    response.email,
                    response.password,
                    response.confirmation,
                )
                self._authenticated_home()
        except AuthenticationError as error:
            self._navigator.set_authentication(
                step=self._navigator.authentication_step,
                email=self._navigator.email or response.email,
                error=authentication_message(error),
            )
        except ValueError as error:
            self._navigator.set_authentication(
                step=self._navigator.authentication_step,
                email=self._navigator.email or response.email,
                error=str(error),
            )
        except Exception:
            logger.exception("Falha ao executar o fluxo de autenticação.")
            self._navigator.set_authentication(
                step=self._navigator.authentication_step,
                email=self._navigator.email or response.email,
                error=(
                    "Não foi possível acessar a autenticação. "
                    "Verifique a configuração local do banco de dados."
                ),
            )

        st.rerun()

    def _authenticated_home(self) -> None:
        self._navigator.open_module("home")
        self._navigator.set_authentication(step="homepage", email="")
