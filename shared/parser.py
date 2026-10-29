"""Conversão e validação de entradas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ParseResult[T]:

    value: T | None
    valid: bool
    message: str | None = None


class Parser:

    # ==========================================================
    # NUMBERS
    # ==========================================================

    @staticmethod
    def integer(
        value: str,
    ) -> ParseResult[int]:

        value = value.strip()

        if not value:

            return ParseResult(
                value=None,
                valid=False,
                message="Informe um número inteiro.",
            )

        value = (
            value
            .replace(".", "")
            .replace(",", "")
        )

        try:

            return ParseResult(
                value=int(value),
                valid=True,
            )

        except ValueError:

            return ParseResult(
                value=None,
                valid=False,
                message="Número inteiro inválido.",
            )

    @staticmethod
    def decimal(
        value: str,
    ) -> ParseResult[float]:

        value = value.strip()

        if not value:

            return ParseResult(
                value=None,
                valid=False,
                message="Informe um valor.",
            )

        value = value.replace(",", ".")

        try:

            return ParseResult(
                value=float(value),
                valid=True,
            )

        except ValueError:

            return ParseResult(
                value=None,
                valid=False,
                message="Valor decimal inválido.",
            )

    # ==========================================================
    # DATE
    # ==========================================================

    @staticmethod
    def datetime(
        value: str,
    ) -> ParseResult[datetime]:

        value = value.strip()

        if not value:

            return ParseResult(
                value=None,
                valid=False,
                message="Informe a data e hora.",
            )

        formats = (

            "%d/%m/%Y %H:%M",

            "%d/%m/%Y %H:%M:%S",

            "%Y-%m-%d %H:%M",

            "%Y-%m-%d %H:%M:%S",

            "%d-%m-%Y %H:%M",

            "%Y/%m/%d %H:%M",

        )

        for fmt in formats:

            try:

                return ParseResult(
                    value=datetime.strptime(
                        value,
                        fmt,
                    ),
                    valid=True,
                )

            except ValueError:

                pass

        return ParseResult(
            value=None,
            valid=False,
            message=(
                "Data e hora inválidas. Use "
                "DD/MM/AAAA HH:MM."
            ),
        )

    @staticmethod
    def timestamp(
        value: str,
    ) -> ParseResult[datetime]:

        value = value.strip()

        if not value:

            return ParseResult(
                value=None,
                valid=False,
                message="Informe uma data.",
            )

        formats = (

            "%Y-%m-%d",

            "%d/%m/%Y",

            "%d-%m-%Y",

            "%Y/%m/%d",

        )

        for fmt in formats:

            try:

                return ParseResult(
                    value=datetime.strptime(
                        value,
                        fmt,
                    ),
                    valid=True,
                )

            except ValueError:

                pass

        return ParseResult(
            value=None,
            valid=False,
            message="Data inválida.",
        )
