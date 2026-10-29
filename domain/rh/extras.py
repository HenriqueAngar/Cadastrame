"""Regras de domínio do cadastro manual de extras."""

from __future__ import annotations

from shared.records import Records


class Extras:

    def __init__(
        self,
        repository,
    ) -> None:

        self._repository = repository

    def identificar(
        self,
        records: Records,
    ) -> Records:

        for record in records.data:

            idcolaborador = record["idcolaborador"]

            record["idcolaborador"] = self._repository.find_idcolaborador(

                idcolaborador,

            )

            if record["idcolaborador"] is None:

                raise ValueError(

                    f"Colaborador {idcolaborador} não encontrado, inativo ou com identificação ambígua entre empresas."

                )

            competencia = record["competencia"].replace(day=1)
            record["competencia"] = competencia
            centros = self._repository.find_centros_colaborador(
                idcolaborador,
                competencia,
            )

            referencia = competencia.strftime("%m/%Y")
            if not centros or any(centro[0] is None or centro[1] is None for centro in centros):
                raise ValueError(
                    f"Não foi possível identificar o centro de custo do colaborador "
                    f"{idcolaborador} na competência {referencia}. "
                    "Verifique a folha e o mapeamento de centros dessa competência."
                )
            if len(centros) != 1:
                raise ValueError(
                    f"O colaborador {idcolaborador} possui mais de um centro de custo "
                    f"na competência {referencia}. Revise o vínculo antes de lançar o extra."
                )

            record["idcentrocusto"], record["codigocentrocusto"] = centros[0]

        return records

    def registrar(
        self,
        records: Records,
    ) -> int:

        total = 0

        for record in records.data:

            self._repository.upsert_extra(

                idcolaborador=record["idcolaborador"],
                idcentrocusto=record["idcentrocusto"],
                codigocentrocusto=record["codigocentrocusto"],
                competencia=record["competencia"],
                horasextras=record["horasextras"],
                valoresextras=record["valoresextras"],
                observacao=record["observacao"],

            )

            total += 1

        return total
