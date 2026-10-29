"""Domínio de preços de produtos."""

from __future__ import annotations

from shared.records import Records


class BasePrecos:

    def __init__(
        self,
        repository,
    ) -> None:

        self._repository = repository

    # ==========================================================
    # BUSINESS
    # ==========================================================

    def identificar(
        self,
        records: Records,
    ) -> Records:
        """
        Identifica o ID do produto para
        cada registro informado.
        """

        for record in records.data:

            record["idproduto"] = self._repository.find_idproduto(

                record["codproduto"],

            )

        return records

    def substituir(
        self,
        records: Records,
    ) -> int:
        """
        Substitui os preços dos produtos
        pelos registros informados.
        """

        total = 0

        for record in records.data:

            self._repository.delete_periodo(

                idproduto=record["idproduto"],

                datainicio=record["datainicio"],

                datafim=record["datafim"],

            )

            self._repository.insert(

                idproduto=record["idproduto"],

                datainicio=record["datainicio"],

                datafim=record["datafim"],

                preco=record["preco"],

            )

            total += 1

        return total