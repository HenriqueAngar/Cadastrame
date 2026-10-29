"""Repositório do módulo Produção."""

from __future__ import annotations

from datetime import datetime

from repositories.base_repository import Repository
from repositories.producao import queries


class ProducaoRepository(Repository):

    # ==========================================================
    # SELECT
    # ==========================================================

    def get_idordemproducao(
        self,
        codop: int,
    ) -> int | None:

        with self.cursor() as cur:

            cur.execute(

                queries.GET_IDORDEMPRODUCAO,

                (codop,),

            )

            row = cur.fetchone()

            return (

                None

                if row is None

                else row[0]

            )

    def get_next_idensaque(
        self,
    ) -> int:

        with self.cursor() as cur:

            cur.execute(

                queries.GET_NEXT_IDENSAQUE,

            )

            return cur.fetchone()[0]

    def get_next_idoutput(
        self,
    ) -> int:

        with self.cursor() as cur:

            cur.execute(

                queries.GET_NEXT_IDOUTPUT,

            )

            return cur.fetchone()[0]

    # ==========================================================
    # INSERT
    # ==========================================================

    def insert_ensaque(
        self,
        *,
        dataensaque: datetime,
        idop: int,
        idproduto: int,
        codop: int,
        codproduto: int,
        turno: int,
        linha: str,
        quantidade: float,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(

                queries.INSERT_ENSAQUE,

                (

                    self.get_next_idensaque(),

                    dataensaque,

                    idop,
                    idproduto,
                    codop,
                    codproduto,
                    turno,
                    linha,
                    quantidade,

                ),

            )

    def insert_output(
        self,
        *,
        dataentrada: datetime,
        idop: int,
        idproduto: int,
        codop: int,
        codproduto: int,
        turno: int,
        linha: str,
        producao: float,
        reprocesso: float,
        motivoreprocesso: str | None,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(

                queries.INSERT_OUTPUT,

                (

                    self.get_next_idoutput(),

                    dataentrada,

                    idop,
                    idproduto,
                    codop,
                    codproduto,
                    turno,
                    linha,
                    producao,
                    reprocesso,
                    motivoreprocesso,

                ),

            )

    def insert_parada(
        self,
        *,
        datahorainicio: datetime,
        datahorafim: datetime,
        linha: str,
        tipoparada: str,
        motivoparada: str,
        observacao: str,
    ) -> None:

        with self.cursor() as cur:

            cur.execute(

                queries.INSERT_PARADA,

                (

                    datahorainicio,
                    datahorafim,
                    linha,
                    tipoparada,
                    motivoparada,
                    observacao,

                ),

            )