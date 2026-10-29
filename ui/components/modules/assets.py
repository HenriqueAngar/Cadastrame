"""Assets de um módulo."""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

import streamlit as st

from shared.records import Records

from ui.components.editor.editor import (
    Editor,
    EditorAction,
)
from ui.components.form.form import FormDefinition


# ==========================================================
# ASSET
# ==========================================================

@dataclass(slots=True)
class Asset:
    """
    Define um asset pertencente a um módulo.

    Um asset é composto por:

        • Definição

        • Formulário

        • Editor (opcional)
    """

    editor: bool = True

    order: int = 0

    _editor: Editor | None = field(
        init=False,
        default=None,
    )

    def __post_init__(
        self,
    ) -> None:

        if self.editor:

            self._editor = Editor(

                key=self.definition.key,

            )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def definition(
        self,
    ) -> FormDefinition:

        return type(self).DEFINITION

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def respond(
        self,
        *,
        context: Records | None = None,
        records: Records | None = None,
        submitted: bool = False,
        **kwargs,
    ) -> Records | str | None:

        response = self.render_form(

            context=context,

            records=records,

            **kwargs,

        )

        #
        # Assets sem editor (Home).
        #

        if not self.editor:

            return response

        #
        # Assets de navegação.
        #

        if isinstance(

            response,

            str,

        ):

            return response

        #
        # Mantém o buffer da sessão.
        #

        if response is not None:

            records = response

        assert records is not None

        action = self._editor.render(

            records,

            submitted=submitted,

            validator=self.validate_records,

        )

        match action:

            case EditorAction.SUBMIT:

                errors = self.validate_records(

                    records,

                )

                if errors:

                    for error in errors:

                        st.error(error)

                    return None

                return records

            case _:

                return None

    # ==========================================================
    # FORM
    # ==========================================================

    def validate_records(
        self,
        records: Records,
    ) -> list[str]:

        return records.validate()

    def render_form(
        self,
        *,
        context: Records | None = None,
        records: Records | None = None,
        **kwargs,
    ) -> Records | str | None:

        raise NotImplementedError


# ==========================================================
# REGISTRY
# ==========================================================

class AssetRegistry:
    """
    Catálogo de assets de um módulo.
    """

    def __init__(
        self,
        *assets: Asset,
    ):

        self._assets = tuple(

            assets,

        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def all(
        self,
    ) -> tuple[Asset, ...]:

        return self._assets

    def allowed(
        self,
        resources: set[int],
        authenticated: bool | None = None,
    ) -> tuple[Asset, ...]:
        """
        Retorna os assets permitidos,
        ordenados conforme definido
        no catálogo.
        """

        if authenticated is None:

            authenticated = bool(resources)

        return tuple(

            sorted(

                (

                    asset

                    for asset in self._assets

                    if (

                        asset.definition.resource_id

                        in resources

                    )

                    or (

                        not authenticated

                        and asset.definition.resource_id == 1

                    )

                ),

                key=lambda asset: asset.order,

            )

        )

    def by_keys(
        self,
        *keys: str,
        resources: set[int] | None = None,
        authenticated: bool | None = None,
    ) -> tuple[Asset, ...]:

        keys = set(

            keys,

        )

        assets = self._assets

        if resources is not None:

            assets = self.allowed(

                resources,

                authenticated=authenticated,

            )

        return tuple(

            asset

            for asset in assets

            if asset.definition.key in keys

        )
