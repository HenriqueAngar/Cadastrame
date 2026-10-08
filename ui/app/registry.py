"""Registro de módulos e autorização por recurso do usuário."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from infraesctruture.auth.utils.models import Resource
from ui.components.modules.module import ModuleDefinition
from ui.modules.estoque.estoque_module import EstoqueModule
from ui.modules.home.home_module import HomeModule
from ui.modules.pcp.pcp_module import PCPModule


@dataclass(frozen=True, slots=True)
class ModuleRegistration:
    definition: ModuleDefinition
    module: Type

    @property
    def label(self) -> str:
        return f"{self.definition.icon} {self.definition.title}"


MODULES = (
    ModuleRegistration(
        definition=ModuleDefinition(
            key="home",
            title="Cadastra.me",
            icon="📥",
            navigator=False,
        ),
        module=HomeModule,
    ),
    ModuleRegistration(
        definition=ModuleDefinition(
            key="estoque",
            title="Estoque",
            icon="📦",
            resource_page_code="estoque",
        ),
        module=EstoqueModule,
    ),
    ModuleRegistration(
        definition=ModuleDefinition(
            key="pcp",
            title="PCP",
            icon="📋",
            resource_page_code="pcp",
        ),
        module=PCPModule,
    ),
)


class ModuleRegistry:
    """Resolve módulos e libera somente os associados aos recursos."""

    def all(self) -> tuple[ModuleRegistration, ...]:
        return MODULES

    def allowed(
        self,
        resources: tuple[Resource, ...] = (),
        *,
        authenticated: bool = False,
    ) -> tuple[ModuleRegistration, ...]:
        home = self.by_key("home")
        if not authenticated:
            return (home,)

        page_codes = {resource.page_code.strip().casefold() for resource in resources}
        return tuple(
            registration
            for registration in MODULES
            if registration.definition.key == "home"
            or registration.definition.resource_page_code in page_codes
        )

    def by_key(self, key: str) -> ModuleRegistration:
        for registration in self.all():
            if registration.definition.key == key:
                return registration
        raise ValueError(f"Módulo '{key}' não encontrado.")

    def index(
        self,
        key: str,
        registrations: tuple[ModuleRegistration, ...] | None = None,
    ) -> int:
        for index, registration in enumerate(registrations or self.all()):
            if registration.definition.key == key:
                return index
        return 0
