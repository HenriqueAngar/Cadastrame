"""Componente de seleção pesquisável."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from repositories.base_repository import (
    Repository,
)


# ==========================================================
# OPTION
# ==========================================================

@dataclass(slots=True, frozen=True)
class SearchOption:
    """
    Opção disponível para seleção.
    """

    key: object

    value: object

    display: str


# ==========================================================
# SEARCH INPUT
# ==========================================================

class SearchInput:
    """
    Componente de seleção pesquisável baseado
    em uma tabela do banco.

    Pode operar de duas formas:

        • Sem código:

          Exibe:
              descrição

          Retorna:
              descrição

        • Com código:

          Exibe:
              código - descrição

          Retorna:
              código

    Os dados são carregados através do
    Repository base utilizando o contrato:

        • chavecampo
        • codigocampo
        • descricaocampo
    """

    def __init__(
        self,
        *,
        schema: str,
        table: str,
        key_field: str,
        description_field: str,
        code_field: str | None = None,
        params: dict | None = None,
    ) -> None:

        self._schema = schema

        self._table = table

        self._key_field = key_field

        self._code_field = code_field

        self._description_field = description_field

        self._params = params

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def render(
        self,
        *,
        label: str,
        key: str,
        allow_new: bool = False,
        placeholder: str = "Selecione uma opção",
        disabled: bool = False,
    ) -> object | None:

        table = self._load()

        options = self._options(

            table,

        )

        values = {

            option.display: option.value

            for option in options

        }

        selected = st.selectbox(

            label,

            options=list(

                values.keys()

            ),

            index=None,

            key=key,

            placeholder=placeholder,

            disabled=disabled,

            accept_new_options=allow_new,

        )

        if selected is None:

            return None

        #
        # Opção já existente.
        #

        if selected in values:

            return values[selected]

        #
        # Nova opção digitada pelo usuário.
        #

        value = selected.strip()

        return (

            value

            if value

            else None

        )

    # ==========================================================
    # LOAD
    # ==========================================================

    def _load(
    self,
    ):

        repository = Repository()

        return repository.search_input(

            schema=self._schema,

            table=self._table,

            key_field=self._key_field,

            code_field=self._code_field,

            description_field=self._description_field,

            params=self._params,

        )

    # ==========================================================
    # OPTIONS
    # ==========================================================

    def _options(
        self,
        table,
    ) -> list[SearchOption]:

        options = []

        for _, row in table.iterrows():

            key = self._value(

                row["chavecampo"]

            )

            description = self._value(

                row["descricaocampo"]

            )

            #
            # Uma coluna.
            #

            if self._code_field is None:

                value = description

                display = str(

                    description

                )

            #
            # Código + descrição.
            #

            else:

                code = self._value(

                    row["codigocampo"]

                )

                value = code

                display = (

                    f"{code} - "
                    f"{description}"

                )

            options.append(

                SearchOption(

                    key=key,

                    value=value,

                    display=display,

                )

            )

        return options

    # ==========================================================
    # VALUE
    # ==========================================================

    @staticmethod
    def _value(
        value: object,
    ) -> object:

        if hasattr(

            value,

            "item",

        ):

            try:

                return value.item()

            except ValueError:

                pass

        return value