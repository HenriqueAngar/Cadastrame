"""Registro dos módulos da aplicação."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Type

# MODULES
from ui.modules.home.home_module import HomeModule
from ui.modules.pcp.pcp_module import PCPModule
from ui.modules.producao.producao_module import ProducaoModule
from ui.modules.rh.rh_module import RHModule


# ==========================================================
# MODULE
# ==========================================================

@dataclass(slots=True, frozen=True)
class Module:

    key: str

    name: str

    icon: str

    module: Type

    resource_id: int | None = None

    @property
    def label(
        self,
    ) -> str:

        return f"{self.icon} {self.name}"


# ==========================================================
# MODULES
# ==========================================================

MODULES = (

    Module(

        key="home",

        name="Cadastra.me",

        icon="📥",

        module=HomeModule,

    ),

    Module(

        key="pcp",

        name="PCP",

        icon="📋",

        module=PCPModule,

        resource_id=2,

    ),

    Module(

        key="producao",

        name="Produção",

        icon="🏭",

        module=ProducaoModule,

        resource_id=3,

    ),

    Module(

        key="rh",

        name="RH",

        icon="👥",

        module=RHModule,

        resource_id=8,

    ),

)


# ==========================================================
# REGISTRY
# ==========================================================

class ModuleRegistry:

    def __init__(self):

        self._modules = MODULES

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def all(
        self,
    ) -> tuple[Module, ...]:

        return self._modules

    def allowed(
        self,
        resources: set[int],
    ) -> tuple[Module, ...]:
        """Retorna somente os módulos autorizados pelos recursos da sessão.

        O módulo inicial é público. Todos os demais precisam possuir o
        recurso de página correspondente; ter acesso a outro módulo ou a um
        formulário não concede acesso implícito ao RH.
        """

        return tuple(

            module

            for module in self._modules

            if (

                module.resource_id is None

                or module.resource_id in resources

            )

        )

    def by_key(
        self,
        key: str,
    ) -> Module:

        for module in self._modules:

            if module.key == key:

                return module

        raise ValueError(

            f"Módulo '{key}' não encontrado."

        )

    def index(
        self,
        key: str,
        modules: tuple[Module, ...],
    ) -> int:
        for index, module in enumerate(

            modules,

        ):

            if module.key == key:

                return index

        return 0
