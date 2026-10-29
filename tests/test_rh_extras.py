"""Regressões do contrato de entrada dos extras de folha."""

import unittest
from datetime import date
from unittest.mock import Mock

from domain.rh.extras import Extras

from shared.records import Column, ColumnType, Records
from ui.modules.rh.assets.extras import ExtrasAsset


class ExtrasInputTests(unittest.TestCase):
    def test_pending_extra_does_not_require_database_creation_timestamp(self):
        records = Records(
            columns=ExtrasAsset.DEFINITION.columns,
            data=[{
                "idcolaborador": 14,
                "idcentrocusto": None,
                "codigocentrocusto": 349423,
                "competencia": date(2026, 10, 1),
                "horasextras": 1,
                "valoresextras": 1,
                "observacao": None,
            }],
        )

        self.assertEqual(records.validate(), [])
        records.from_dataframe(records.to_dataframe())
        self.assertEqual(records.validate(), [])
        self.assertEqual(ExtrasAsset().validate_records(records), [])

    def test_user_entered_datetimes_are_still_required(self):
        records = Records(
            columns={"inicio": Column(type=ColumnType.DATETIME)},
            data=[{"inicio": None}],
        )

        self.assertEqual(records.validate(), ["Registro 1: informe inicio."])




class ExtrasCompetenciaTests(unittest.TestCase):
    def test_default_is_previous_month(self):
        self.assertEqual(
            ExtrasAsset.competencia_padrao(date(2026, 10, 26)),
            date(2026, 9, 1),
        )

    def test_january_defaults_to_december_previous_year(self):
        self.assertEqual(
            ExtrasAsset.competencia_padrao(date(2026, 1, 1)),
            date(2025, 12, 1),
        )

    def test_march_after_leap_february(self):
        self.assertEqual(
            ExtrasAsset.competencia_padrao(date(2024, 3, 31)),
            date(2024, 2, 1),
        )

    def setUp(self):
        self.repository = Mock()
        self.repository.find_idcolaborador.return_value = 123
        self.repository.find_centros_colaborador.return_value = [(902, 349423)]
        self.domain = Extras(self.repository)
        self.records = Records(data=[{
            "idcolaborador": 123,
            "competencia": date(2026, 9, 1),
            "horasextras": 2,
            "valoresextras": 50,
            "observacao": None,
        }])

    def test_resolves_and_saves_center_for_exact_competence(self):
        self.domain.identificar(self.records)
        self.assertEqual(self.domain.registrar(self.records), 1)
        self.repository.find_centros_colaborador.assert_called_once_with(
            123, date(2026, 9, 1),
        )
        saved = self.repository.upsert_extra.call_args.kwargs
        self.assertEqual(saved["idcentrocusto"], 902)
        self.assertEqual(saved["codigocentrocusto"], 349423)
        self.assertEqual(saved["idcolaborador"], 123)

    def test_does_not_fall_back_to_previous_payroll_when_month_missing(self):
        self.repository.find_centros_colaborador.return_value = []
        with self.assertRaisesRegex(ValueError, "09/2026"):
            self.domain.identificar(self.records)
        self.repository.upsert_extra.assert_not_called()
        self.repository.find_centros_colaborador.assert_called_once()

    def test_rejects_multiple_centers(self):
        self.repository.find_centros_colaborador.return_value = [(902, 349423), (903, 349424)]
        with self.assertRaisesRegex(ValueError, "mais de um centro"):
            self.domain.identificar(self.records)
        self.repository.upsert_extra.assert_not_called()

    def test_rejects_missing_mapping(self):
        self.repository.find_centros_colaborador.return_value = [(None, None)]
        with self.assertRaisesRegex(ValueError, "mapeamento"):
            self.domain.identificar(self.records)

    def test_rejects_invalid_or_ambiguous_employee(self):
        self.repository.find_idcolaborador.return_value = None
        with self.assertRaisesRegex(ValueError, "ambígua"):
            self.domain.identificar(self.records)
        self.repository.find_centros_colaborador.assert_not_called()


class ExtrasFormTests(unittest.TestCase):
    def test_form_adds_auto_center_and_previous_month_without_center_input(self):
        from streamlit.testing.v1 import AppTest

        script = r"""
import streamlit as st
import pandas as pd
from datetime import date
from unittest.mock import patch
from shared.records import Records
from ui.modules.rh.assets.extras import ExtrasAsset

if "records" not in st.session_state:
    st.session_state.records = Records(columns=ExtrasAsset.DEFINITION.columns)

options = pd.DataFrame([{
    "chavecampo": 123, "codigocampo": 123, "descricaocampo": "Colaborador teste",
}])
with patch("repositories.rh.rh_repository.RHRepository.list_colaboradores_extras", return_value=[(123, "Colaborador teste")]), \
     patch("repositories.rh.rh_repository.RHRepository.find_idcolaborador", return_value=123), \
     patch("repositories.rh.rh_repository.RHRepository.find_centros_colaborador", return_value=[(902, 349423)]), \
     patch("ui.modules.rh.assets.extras.date", wraps=date) as clock:
    clock.today.return_value = date(2026, 10, 26)
    ExtrasAsset().respond(records=st.session_state.records)
"""
        app = AppTest.from_string(script).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.selectbox(key="extras_mes_competencia").value, 9)
        self.assertEqual(app.selectbox(key="extras_ano_competencia").value, 2026)
        self.assertEqual(app.selectbox(key="extras_mes_competencia").options[8], "Setembro")
        self.assertFalse(any(item.label == "Centro de custo" for item in app.selectbox))
        app.selectbox(key="extras_colaborador").select((123, "Colaborador teste"))
        app.text_input(key="extras_horas").set_value("2")
        app.text_input(key="extras_valor").set_value("50")
        next(button for button in app.button if "Adicionar" in button.label).click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.error), 0)
        record = app.session_state["records"].data[0]
        self.assertEqual(record["competencia"], date(2026, 9, 1))
        self.assertEqual(record["idcentrocusto"], 902)
        self.assertEqual(record["codigocentrocusto"], 349423)


if __name__ == "__main__":
    unittest.main()
