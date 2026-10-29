"""Navegação entre formulários de um módulo."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from ui.components.modules.assets import Asset


# ==========================================================
# RESULT
# ==========================================================

@dataclass(slots=True, frozen=True)
class NavigationResult:

    asset: Asset

    changed: bool


# ==========================================================
# NAVIGATOR
# ==========================================================

class FormNavigator:
    """
    Responsável pela navegação entre
    os assets de um módulo.
    """

    def __init__(
        self,
        key: str,
    ):

        self._key = key

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def render(
        self,
        assets: tuple[Asset, ...],
    ) -> NavigationResult:

        if not assets:

            raise ValueError(

                "Nenhum formulário disponível.",

            )

        self._initialize(

            assets,

        )

        previous = self.selected

        columns = st.columns(

            len(assets),

        )

        for column, asset in zip(

            columns,
            assets,

        ):

            definition = asset.definition

            if column.button(

                definition.label,

                use_container_width=True,

                type=(

                    "primary"

                    if definition.key == self.selected

                    else "secondary"

                ),

            ):

                #
                # Mudou de formulário.
                #

                if definition.key != self.selected:

                    self.selected = definition.key

                    self.submitted = False

        current = self.current(

            assets,

        )

        return NavigationResult(

            asset=current,

            changed=current.definition.key != previous,

        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _initialize(
        self,
        assets: tuple[Asset, ...],
    ) -> None:

        if self._state_key not in st.session_state:

            self.selected = assets[0].definition.key

        if self._submitted_key not in st.session_state:

            self.submitted = False

    def current(
        self,
        assets: tuple[Asset, ...],
    ) -> Asset:

        for asset in assets:

            if asset.definition.key == self.selected:

                return asset

        self.selected = assets[0].definition.key

        self.submitted = False

        return assets[0]

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def _state_key(
        self,
    ) -> str:

        return f"{self._key}:form"

    @property
    def _submitted_key(
        self,
    ) -> str:

        return f"{self._key}:submitted"

    @property
    def selected(
        self,
    ) -> str:

        return st.session_state[
            self._state_key
        ]

    @selected.setter
    def selected(
        self,
        value: str,
    ) -> None:

        st.session_state[
            self._state_key
        ] = value

    @property
    def submitted(
        self,
    ) -> bool:

        return st.session_state.get(

            self._submitted_key,

            False,

        )

    @submitted.setter
    def submitted(
        self,
        value: bool,
    ) -> None:

        st.session_state[
            self._submitted_key
        ] = value