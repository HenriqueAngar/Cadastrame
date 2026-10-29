"""Domínio da Produção."""

from __future__ import annotations

from datetime import datetime

from shared.records import Records


class Producao:

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

        for record in records.data:

            record["idproduto"] = (
                self._repository.find_idproduto(
                    record["codproduto"],
                )
            )

            record["idop"] = (
                self._repository.get_idordemproducao(
                    record["codop"],
                )
            )

            if record["idproduto"] is None:

                raise ValueError(

                    f"Produto "
                    f"{record['codproduto']} "
                    "não encontrado."

                )

            if record["idop"] is None:

                raise ValueError(

                    f"OP "
                    f"{record['codop']} "
                    "não encontrada."

                )

        return records

    # ==========================================================
    # ENSAQUES
    # ==========================================================

    def registrar_ensaques(
        self,
        records: Records,
    ) -> int:

        total = 0

        for record in records.data:

            self._repository.insert_ensaque(

                dataensaque=record["data"],
                idop=record["idop"],
                idproduto=record["idproduto"],
                codop=record["codop"],
                codproduto=record["codproduto"],
                turno=record["turno"],
                linha=record["linha"],
                quantidade=record["quantidade"],

            )

            total += 1

        return total

    # ==========================================================
    # PRODUÇÃO
    # ==========================================================

    def registrar_producao(
        self,
        records: Records,
    ) -> int:

        total = 0

        for record in records.data:

            self._repository.insert_output(

                dataentrada=record["data"],
                idop=record["idop"],
                idproduto=record["idproduto"],
                codop=record["codop"],
                codproduto=record["codproduto"],
                turno=record["turno"],
                linha=record["linha"],
                producao=record["producao"],
                reprocesso=record["reprocesso"],
                motivoreprocesso=record["motivoreprocesso"],

            )

            total += 1

        return total

    # ==========================================================
    # PARADAS
    # ==========================================================

    def registrar_paradas(
        self,
        records: Records,
    ) -> int:

        total = 0

        for index, record in enumerate(
            records.data,
            start=1,
        ):

            datahorainicio = record["datahorainicio"]

            datahorafim = record["datahorafim"]

            if not isinstance(datahorainicio, datetime):

                raise ValueError(
                    f"Registro {index}: data/hora inicial inválida."
                )

            if not isinstance(datahorafim, datetime):

                raise ValueError(
                    f"Registro {index}: data/hora final inválida."
                )

            if datahorafim <= datahorainicio:

                raise ValueError(
                    f"Registro {index}: a data/hora final deve "
                    "ser posterior à inicial."
                )

            self._repository.insert_parada(

                datahorainicio=datahorainicio,
                datahorafim=datahorafim,
                linha=record["linha"],
                tipoparada=record["tipoparada"],
                motivoparada=record["motivoparada"],
                observacao=record["observacao"],

            )

            total += 1

        return total
