"""Repositório de custos de produtos."""

from __future__ import annotations

from datetime import date

from domain.pcp.models import BasePreco

from repositories.base import Repository
from repositories.pcp import queries


class BasePrecosRepository(Repository):

    # ==========================================================
    # SELECT
    # ==========================================================

    def get_idproduto(
        self,
        codproduto: int,
    ) -> int | None:

        with self.cursor() as cur:

            cur.execute(
                queries.GET_IDPRODUTO,
                (codproduto,),
            )

            row = cur.fetchone()

            if row is None:
                return None

            return row[0]

    def get_next_idprecoref(
        self,
    ) -> int:

        with self.cursor() as cur:

            cur.execute(
                queries.GET_NEXT_IDPRECOREF,
            )

            return cur.fetchone()[0]

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_periodo(
        self,
        idproduto: int,
        datainicio: date,
        datafim: date,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(
                queries.DELETE_PERIODO,
                (
                    idproduto,
                    datainicio,
                    datafim,
                ),
            )

    # ==========================================================
    # INSERT
    # ==========================================================

    def insert(
        self,
        registro: BasePreco,
    ) -> None:

        idprecoref = self.get_next_idprecoref()

        with self.cursor() as cur:

            cur.execute(
                queries.INSERT,
                (
                    idprecoref,
                    registro.idproduto,
                    registro.datainicio,
                    registro.datafim,
                    registro.preco,
                ),
            )