"""Verificações opcionais com dados reais, sempre em transação somente leitura.

RH_RUN_DB_TESTS=1 habilita; RH_DB_TEST_TARGET escolhe teste ou warehouse.
"""

import json
import os
import unittest
from contextlib import contextmanager
from pathlib import Path

import psycopg

from domain.rh.extras import Extras
from repositories.rh.rh_repository import RHRepository
from shared.records import Records


@unittest.skipUnless(os.environ.get("RH_RUN_DB_TESTS") == "1", "Banco real: execução explícita")
class ExtrasDatabaseTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        configs = json.loads(
            (root / "infraesctruture/configs/secrets.json").read_text(encoding="utf-8-sig")
        )["databases"]
        config = configs[os.environ.get("RH_DB_TEST_TARGET", "teste")]
        self.connection = psycopg.connect(
            host=config["host"], port=config["port"], dbname=config["database"],
            user=config["user"], password=config["password"], connect_timeout=8,
            options="-c default_transaction_read_only=on",
        )
        self.addCleanup(self.connection.close)
        connection = self.connection

        class ReadOnlyRepository(RHRepository):
            @contextmanager
            def cursor(self):
                with connection.cursor() as cursor:
                    yield cursor

        self.repository = ReadOnlyRepository()

    def test_every_offered_employee_passes_real_identification(self):
        employees = self.repository.list_colaboradores_extras()
        self.assertTrue(employees)
        for employee_id, _ in employees:
            with self.subTest(idcolaborador=employee_id):
                self.assertEqual(self.repository.find_idcolaborador(employee_id), employee_id)

    def test_real_payroll_resolves_center_without_manual_input(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT max(competencia) FROM pdrh.folhas WHERE idextra IS NULL")
            competence = cursor.fetchone()[0]
        resolved = 0
        for employee_id, _ in self.repository.list_colaboradores_extras():
            centers = self.repository.find_centros_colaborador(employee_id, competence)
            if len(centers) != 1 or any(value is None for value in centers[0]):
                continue
            records = Records(data=[{
                "idcolaborador": employee_id, "competencia": competence,
            }])
            Extras(self.repository).identificar(records)
            self.assertEqual(
                (records.data[0]["idcentrocusto"], records.data[0]["codigocentrocusto"]),
                centers[0],
            )
            resolved += 1
        self.assertGreater(resolved, 0)
