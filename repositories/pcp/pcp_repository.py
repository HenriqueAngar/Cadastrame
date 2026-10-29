"""Repositório de custos de produtos."""

from __future__ import annotations

from datetime import date

from repositories.base_repository import Repository
from repositories.pcp import pcp_queries


class BasePrecosRepository(Repository):

    # ==========================================================
    # SELECT
    # ==========================================================

    def get_next_idprecoref(
        self,
    ) -> int:

        with self.cursor() as cur:

            cur.execute(

                pcp_queries.GET_NEXT_IDPRECOREF,

            )

            return cur.fetchone()[0]

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_periodo(
        self,
        *,
        idproduto: int,
        datainicio: date,
        datafim: date,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(

                pcp_queries.DELETE_PERIODO,

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
        *,
        idproduto: int,
        datainicio: date,
        datafim: date,
        preco: float,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(

                pcp_queries.INSERT,

                (

                    self.get_next_idprecoref(),

                    idproduto,
                    datainicio,
                    datafim,
                    preco,

                ),

            )