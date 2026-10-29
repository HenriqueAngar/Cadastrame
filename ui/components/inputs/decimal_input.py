from __future__ import annotations

import streamlit as st

from shared.parser import (
    Parser,
    ParseResult,
)


class DecimalInput:

    def render(
        self,
        label: str,
        key: str,
        value: str = "",
        placeholder: str = "0,0000",
    ) -> ParseResult[float]:

        text = st.text_input(
            label=label,
            value=value,
            key=key,
            placeholder=placeholder,
        )

        return Parser.decimal(
            text,
        )