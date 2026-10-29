"""Componentes base para formulários."""

from __future__ import annotations

from dataclasses import dataclass, field

from shared.records import Records, Column


# ==========================================================
# DEFINITION
# ==========================================================

@dataclass(slots=True, frozen=True)
class FormDefinition:
    """
    Definição declarativa de um formulário.
    """

    key: str

    title: str

    label: str

    resource_id: int

    columns: dict[str, Column] = field(

        default_factory=dict,

    )

    confirmation: str = (

        "Confirmo o envio dos registros."

    )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def form_key(
        self,
    ) -> str:

        return f"{self.key}_form"

    @property
    def records_key(
        self,
    ) -> str:

        return f"{self.key}_records"

    @property
    def submission_key(
        self,
    ) -> str:

        return f"{self.key}_submission"


# ==========================================================
# FORM
# ==========================================================

from typing import ClassVar

@dataclass(slots=True)
class Form:

    """
    Componente base para formulários.

    Responsabilidades

        • Renderizar a interface

        • Coletar os dados informados

        • Retornar os registros produzidos

    O processamento pertence ao módulo,
    através do respectivo serviço.
    """

    DEFINITION: ClassVar[FormDefinition]

    definition: FormDefinition

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def render(
        self,
        *,
        context: Records | None = None,
        records: Records | None = None,
        **kwargs,
    ) -> Records | str | None:
        """
        Renderiza o formulário.

        Recebe opcionalmente registros de
        contexto produzidos pela aplicação
        e devolve os registros produzidos
        pelo usuário.
        """

        raise NotImplementedError