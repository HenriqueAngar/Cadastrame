import unittest
from datetime import datetime
from unittest.mock import patch

import pandas as pd

from shared.parser import Parser
from shared.records import Column, ColumnType, Records
from ui.components.inputs.datetime_input import DateTimeInput


class DateTimeParserTests(unittest.TestCase):

    @patch(
        "ui.components.inputs.datetime_input.st.text_input",
        return_value="08/09/2026 16:49",
    )
    def test_component_uses_one_combined_datetime_input(
        self,
        text_input,
    ):
        result = DateTimeInput().render(
            label="Data/Hora",
            key="datetime",
            value=datetime(2026, 9, 8, 16, 49),
        )

        self.assertTrue(result.valid)
        self.assertEqual(
            text_input.call_args.kwargs["value"],
            "08/09/2026 16:49",
        )

    def test_parser_accepts_combined_brazilian_datetime(self):
        result = Parser.datetime("08/09/2026 16:49")

        self.assertTrue(result.valid)
        self.assertEqual(
            result.value,
            datetime(2026, 9, 8, 16, 49),
        )

    def test_parser_rejects_datetime_without_time(self):
        result = Parser.datetime("08/09/2026")

        self.assertFalse(result.valid)
        self.assertIsNone(result.value)


class RecordsDateTimeTests(unittest.TestCase):

    def setUp(self):
        self.records = Records(
            columns={
                "datahorainicio": Column(
                    label="Data/Hora Início",
                    type=ColumnType.DATETIME,
                    editable=True,
                ),
            },
        )

    def test_from_dataframe_normalizes_pandas_timestamp(self):
        self.records.from_dataframe(
            pd.DataFrame(
                {
                    "datahorainicio": [
                        pd.Timestamp("2026-09-08 16:49"),
                    ],
                },
            ),
        )

        self.assertIsInstance(
            self.records.data[0]["datahorainicio"],
            datetime,
        )
        self.assertEqual(self.records.validate(), [])

    def test_validate_rejects_invalid_datetime_after_edit(self):
        self.records.from_dataframe(
            pd.DataFrame(
                {
                    "datahorainicio": ["horário inválido"],
                },
            ),
        )

        errors = self.records.validate()

        self.assertEqual(len(errors), 1)
        self.assertIn("data e hora válidas", errors[0])
