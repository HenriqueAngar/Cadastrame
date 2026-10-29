"""Repositório do cadastro manual de extras de folha."""

from __future__ import annotations

from datetime import date

from repositories.base_repository import Repository
from repositories.rh import queries


class RHRepository(Repository):

    def list_colaboradores_extras(self) -> list[tuple[int, str]]:
        with self.cursor() as cur:
            cur.execute(queries.LIST_COLABORADORES_EXTRAS)
            return cur.fetchall()


    def find_idcolaborador(
        self,
        idcolaborador: int,
    ) -> int | None:

        with self.cursor() as cur:

            cur.execute(

                queries.FIND_IDCOLABORADOR,

                (idcolaborador,),

            )

            row = cur.fetchone()

            return None if row is None else row[0]

    def find_centros_colaborador(
        self,
        idcolaborador: int,
        competencia: date,
    ) -> list[tuple[int | None, int | None]]:

        with self.cursor() as cur:
            cur.execute(
                queries.FIND_CENTROS_COLABORADOR,
                (idcolaborador, competencia),
            )
            return cur.fetchall()

    def upsert_extra(
        self,
        *,
        idcolaborador: int,
        idcentrocusto: int,
        codigocentrocusto: int,
        competencia: date,
        horasextras: float,
        valoresextras: float,
        observacao: str | None,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(

                queries.UPSERT_EXTRA,

                (
                    idcolaborador,
                    idcentrocusto,
                    codigocentrocusto,
                    competencia,
                    horasextras,
                    valoresextras,
                    observacao,
                ),

            )
