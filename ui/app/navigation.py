"""Gerenciamento da navegação."""

from __future__ import annotations

import streamlit as st

from infraesctruture.auth.manager import AuthManager
from infraesctruture.auth.utils.handler import AuthenticationError, message
from infraesctruture.connection.config import Settings
from psycopg import Error as DatabaseError

from shared.records import Records

from ui.app.navigator import Navigator
from ui.app.registry import ModuleRegistry


class Navigation:

    def __init__(self):

        self._auth = AuthManager()

        self._navigator = Navigator()

        self._registry = ModuleRegistry()



    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(self) -> None:
        try:
            self._run()
        except AuthenticationError as error:
            st.error(message(error))
        except DatabaseError:
            self._auth.logout()
            self._navigator.clear()
            st.error("Não foi possível validar o acesso. Tente entrar novamente.")

    def _run(
        self,
    ) -> None:

        if self._auth.session.authenticated:
            previous = self._auth.session.user
            if not self._auth.refresh():
                self._navigator.clear()
            else:
                current = self._auth.session.user
                if previous != current:
                    self._navigator.clear()
                    self._navigator.transition("homepage")
                self._auth.session.touch()
                st.sidebar.caption(f"Conectado como {current.username}")
                if st.sidebar.button("Sair", key="auth:logout"):
                    self._auth.logout()
                    self._navigator.clear()
                    st.rerun()

        if Settings().application.environment == "development":
            st.sidebar.caption("Ambiente de desenvolvimento")

        resources = self._resources()

        modules = self._modules()

        if not modules:

            st.error(

                "Nenhum módulo disponível.",

            )

            return

        definition = self._definition(

            modules,

        )

        component = definition.module()

        response = component.respond(

            context=self._navigator.context,

            records=self._navigator.records,

            username=(

                self._auth.session.user.username

                if self._auth.session.authenticated

                else None

            ),

            modules=tuple(

                module

                for module in modules

                if module.key != "home"

            ),

            resources=resources,

            authenticated=self._auth.session.authenticated,

        )

        if definition.key == "home":

            self._home_flow(

                response,

            )

            return

        self._module_flow(

            response,

        )

    # ==========================================================
    # AUTH
    # ==========================================================

    def _authenticate(
        self,
        records: Records,
    ) -> None:

        if records.empty:

            return

        action = records.metadata["key"]

        domain = records.data[0]

        match action:

            case "identify":

                status = self._auth.identify(

                    email=domain.email,

                )

                self._navigator.identify(

                    status,

                    records,

                )

            case "login":

                self._auth.login(

                    email=domain.email,

                    password=domain.value,

                )

                domain.clear()
                self._navigator.clear()
                self._navigator.login(Records())

            case "create_password":

                self._auth.create_password(

                    email=domain.email,

                    password=domain.value,

                )

                domain.clear()
                self._navigator.clear()
                self._navigator.login(Records())

    # ==========================================================
    # MODULES
    # ==========================================================

    def _resources(
        self,
    ) -> set[int]:

        if not self._auth.session.authenticated:

            return set()

        return {

            resource.id

            for resource

            in self._auth.session.user.resources

        }

    def _modules(
        self,
    ):

        return self._registry.allowed(

            self._resources(),

        )

    def _definition(
        self,
        modules,
    ):

        if not self._auth.session.authenticated:

            return self._registry.by_key(

                "home",

            )

        if self._navigator.module is None:

            self._navigator.open_module(

                "home",

            )

        if self._navigator.module == "home":

            return self._registry.by_key(

                "home",

            )

        # Nunca confia apenas no valor persistido em session_state. A lista
        # recebida aqui já foi filtrada pelos recursos do usuário atual.
        # Qualquer módulo antigo, inválido ou não autorizado volta para a
        # página inicial sem sequer renderizar seu componente.
        if not any(

            module.key == self._navigator.module

            for module in modules

        ):

            self._navigator.open_module(

                "home",

            )

            return self._registry.by_key(

                "home",

            )

        return self._sidebar(

            modules,

        )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def _sidebar(
        self,
        modules,
    ):

        available = tuple(

            module

            for module in modules

            if module.key != "home"

        )

        if not available:

            self._navigator.open_module(

                "home",

            )

            return self._registry.by_key(

                "home",

            )

        selected = st.sidebar.radio(

            "Navegação",

            [

                module.label

                for module in available

            ],

            index=self._registry.index(

                self._navigator.module,

                available,

            ),

        )

        module = next(

            module

            for module in available

            if module.label == selected

        )

        self._navigator.open_module(

            module.key,

        )

        return module

    # ==========================================================
    # FLOWS
    # ==========================================================

    def _home_flow(
        self,
        response,
    ) -> None:

        if response is None:

            return

        if isinstance(

            response,

            str,

        ):

            self._navigator.open_module(

                response,

            )

            st.rerun()

            return

        if isinstance(

            response,

            Records,

        ):

            self._authenticate(

                response,

            )

            st.rerun()

    def _module_flow(
        self,
        response,
    ) -> None:
        
        if response is None:

            return

        st.rerun()
