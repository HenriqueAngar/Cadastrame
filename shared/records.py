"""Coleção de registros de um formulário."""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
    is_dataclass,
)

from datetime import datetime

from enum import Enum

import pandas as pd

from shared.parser import Parser


# ==========================================================
# COLUMN TYPE
# ==========================================================

class ColumnType(Enum):
    """
    Tipo semântico de uma coluna.

    Define como consumidores de Records devem interpretar
    e apresentar os valores da coluna.

    O tipo não altera o valor armazenado em Records.
    """

    TEXT = "text"

    NUMBER = "number"

    DATE = "date"

    DATETIME = "datetime"


# ==========================================================
# COLUMN
# ==========================================================

@dataclass(slots=True, frozen=True)
class Column:
    """
    Definição de uma coluna.

    Responsabilidades

        • Definir o rótulo da coluna

        • Informar se o valor pode ser editado

        • Definir largura de apresentação

        • Declarar o tipo semântico do valor

        • Declarar o formato desejado de apresentação

    O formato não modifica o valor armazenado.
    """

    label: str | None = None

    editable: bool = False

    width: str | None = None

    type: ColumnType = ColumnType.TEXT

    format: str | None = None


# ==========================================================
# RECORDS
# ==========================================================

@dataclass(slots=True)
class Records:
    """
    Estrutura e dados de um formulário.

    Responsabilidades

        • Definir as colunas

        • Armazenar os registros

        • Declarar a semântica das colunas

        • Converter registros em DataFrame

        • Atualizar registros a partir de um DataFrame
    """

    columns: dict[str, Column] = field(
        default_factory=dict,
    )

    data: list = field(
        default_factory=list,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def empty(
        self,
    ) -> bool:

        return len(

            self.data,

        ) == 0

    @property
    def size(
        self,
    ) -> int:

        return len(

            self.data,

        )

    @property
    def record_type(
        self,
    ) -> type | None:

        if self.empty:

            return None

        return type(

            self.data[0],

        )

    # ==========================================================
    # COLLECTION
    # ==========================================================

    def __len__(
        self,
    ) -> int:

        return self.size

    def __iter__(
        self,
    ):

        return iter(

            self.data,

        )

    def __getitem__(
        self,
        index: int,
    ):

        return self.data[index]

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def add(
        self,
        record: object,
    ) -> None:

        if (

            not self.empty

            and not isinstance(

                record,

                self.record_type,

            )

        ):

            raise TypeError(

                "Todos os registros devem possuir o mesmo tipo.",

            )

        self.data.append(

            record,

        )

    def extend(
        self,
        records: list,
    ) -> None:

        if not records:

            return

        if (

            not self.empty

            and not all(

                isinstance(

                    record,

                    self.record_type,

                )

                for record in records

            )

        ):

            raise TypeError(

                "Todos os registros devem possuir o mesmo tipo.",

            )

        self.data.extend(

            records,

        )

    def replace(
        self,
        records: list,
    ) -> None:

        self.clear()

        self.extend(

            records,

        )

    def remove(
        self,
        indexes: list[int],
    ) -> None:

        self.data = [

            record

            for index, record

            in enumerate(

                self.data,

            )

            if index not in indexes

        ]

    def clear(
        self,
    ) -> None:

        self.data.clear()

    # ==========================================================
    # DATAFRAME
    # ==========================================================

    def validate(
        self,
    ) -> list[str]:
        """
        Valida os tipos semânticos dos registros.

        Campos DATETIME são normalizados para datetime Python em
        ``from_dataframe``. Ainda assim, a validação permanece aqui
        para impedir que um valor inválido seja enviado ao serviço.
        """

        errors = []

        for index, record in enumerate(
            self.data,
            start=1,
        ):

            for name, column in self.columns.items():

                if column.type is not ColumnType.DATETIME:

                    continue

                value = (
                    record.get(name)
                    if isinstance(record, dict)
                    else getattr(record, name, None)
                )

                if self._is_missing(value):

                    errors.append(
                        f"Registro {index}: informe "
                        f"{column.label or name}."
                    )

                    continue

                if not isinstance(value, datetime):

                    errors.append(
                        f"Registro {index}: {column.label or name} "
                        "deve conter uma data e hora válidas."
                    )

        return errors

    @staticmethod
    def _is_missing(
        value: object,
    ) -> bool:

        if value is None or value is pd.NaT:

            return True

        try:

            return bool(pd.isna(value))

        except (TypeError, ValueError):

            return False

    @staticmethod
    def _normalize_value(
        value: object,
        column: Column | None,
    ) -> object:

        if column is None or column.type is not ColumnType.DATETIME:

            return value

        if Records._is_missing(value):

            return None

        if isinstance(value, pd.Timestamp):

            return value.to_pydatetime()

        if isinstance(value, datetime):

            return value

        if isinstance(value, str):

            parsed = Parser.datetime(value)

            if parsed.valid:

                return parsed.value

        return value

    def to_dataframe(
        self,
    ) -> pd.DataFrame:

        return pd.DataFrame(

            [

                asdict(

                    record,

                )

                if is_dataclass(

                    record,

                )

                else record

                for record in self.data

            ]

        )

    def from_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        rows = dataframe.to_dict(

            orient="records",

        )

        rows = [

            {

                name: self._normalize_value(
                    value,
                    self.columns.get(name),
                )

                for name, value in row.items()

            }

            for row in rows

        ]

        record_type = self.record_type

        if (

            record_type is not None

            and is_dataclass(

                record_type,

            )

        ):

            self.data = [

                record_type(

                    **row,

                )

                for row in rows

            ]

            return

        self.data = rows
