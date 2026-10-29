"""Gerenciador do estado de navegação."""

from __future__ import annotations

import streamlit as st

from infraesctruture.auth.utils.handler import (
    AuthenticationStatus,
)

from shared.records import Records

from ui.components.form.form import FormDefinition
from ui.components.modules.navigator import NavigationResult


class Navigator:
    """
    Gerenciador central do estado da aplicação.

    Responsabilidades

        • Estado do módulo

        • Estado do contexto

        • Buffer de registros

        • Transições da interface

        • Regras de navegação
    """

    def __init__(self):

        st.session_state.setdefault(

            "module",

            None,

        )

        st.session_state.setdefault(

            "context",

            Records(),

        )

        st.session_state.setdefault(

            "records",

            Records(),

        )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def module(
        self,
    ) -> str | None:

        return st.session_state.module

    @property
    def context(
        self,
    ) -> Records:

        return st.session_state.context

    @property
    def records(
        self,
    ) -> Records:

        return st.session_state.records

    @property
    def step(
        self,
    ) -> str:

        return self.context.metadata.get(

            "step",

            "login",

        )

    # ==========================================================
    # MODULE
    # ==========================================================

    def open_module(
        self,
        module: str,
    ) -> bool:
        """
        Seleciona um módulo.

        Returns
        -------
        bool
            True quando houve mudança.
        """

        changed = module != self.module

        if changed:

            st.session_state.module = module

            self.clear_records()

        return changed

    # ==========================================================
    # ASSET
    # ==========================================================

    def open_asset(
        self,
        navigation: NavigationResult,
    ) -> NavigationResult:
        """
        Aplica as regras de abertura de um asset.
        """

        if (

            navigation.changed

            and navigation.asset.definition.editor

        ):

            self.initialize_records(

                navigation.asset.definition,

            )

        return navigation

    # ==========================================================
    # CONTEXT
    # ==========================================================

    def transition(
        self,
        step: str,
        context: Records | None = None,
    ) -> None:

        if context is not None:

            st.session_state.context = context

        st.session_state.context.metadata[

            "step"

        ] = step

    # ==========================================================
    # AUTHENTICATION
    # ==========================================================

    def identify(
        self,
        status: AuthenticationStatus,
        context: Records,
    ) -> None:

        match status:

            case AuthenticationStatus.PASSWORD_REQUIRED:

                self.transition(

                    "password",

                    context,

                )

            case AuthenticationStatus.FIRST_ACCESS:

                self.transition(

                    "create_password",

                    context,

                )

            case AuthenticationStatus.AUTHENTICATED:

                self.transition(

                    "homepage",

                    context,

                )

        self.clear_records()

    def login(
        self,
        context: Records,
    ) -> None:

        self.transition(

            "homepage",

            context,

        )

        self.clear_records()

    def password_created(
        self,
        context: Records,
    ) -> None:

        self.transition(

            "password",

            context,

        )

        self.clear_records()

    # ==========================================================
    # RECORDS
    # ==========================================================

    def initialize_records(
        self,
        definition: FormDefinition,
    ) -> None:
        """
        Inicializa o buffer para um formulário.
        """

        if (

            self.records.columns

            != definition.columns

        ):

            st.session_state.records = Records(

                columns=definition.columns,

            )

    def clear_records(
        self,
    ) -> None:

        self.records.clear()

    # ==========================================================
    # SESSION
    # ==========================================================

    def clear(
        self,
    ) -> None:

        st.session_state.module = None

        context = Records()

        context.metadata["step"] = "login"

        st.session_state.context = context

        st.session_state.records = Records()