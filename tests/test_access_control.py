import unittest
from types import SimpleNamespace

from ui.app.navigation import Navigation
from ui.app.registry import ModuleRegistry
from ui.components.form.form import FormDefinition
from ui.components.modules.assets import Asset, AssetRegistry
from ui.modules.pcp.assets.baseprecos import BasePrecosAsset
from ui.modules.rh.assets.extras import ExtrasAsset


class PublicAsset(Asset):

    DEFINITION = FormDefinition(
        key="public",
        title="Público",
        label="Público",
        resource_id=1,
    )

    def render_form(self, **kwargs):
        return None


class ProtectedAsset(Asset):

    DEFINITION = FormDefinition(
        key="protected",
        title="Protegido",
        label="Protegido",
        resource_id=10,
    )

    def render_form(self, **kwargs):
        return None


class AccessControlTests(unittest.TestCase):

    def test_modules_follow_role_resources(self):
        registry = ModuleRegistry()

        self.assertEqual(
            tuple(module.key for module in registry.allowed({1, 2, 4})),
            ("home", "pcp"),
        )

        self.assertEqual(
            tuple(module.key for module in registry.allowed({1, 3, 5, 6, 7})),
            ("home", "producao"),
        )

    def test_production_role_cannot_open_rh(self):
        registry = ModuleRegistry()
        modules = registry.allowed({1, 3, 5, 6, 7})

        self.assertNotIn("rh", tuple(module.key for module in modules))

    def test_rh_role_cannot_open_production(self):
        registry = ModuleRegistry()
        modules = registry.allowed({1, 8})

        self.assertEqual(
            tuple(module.key for module in modules),
            ("home", "rh"),
        )

    def test_stale_unauthorized_module_returns_to_home(self):
        navigation = Navigation.__new__(Navigation)
        navigator = SimpleNamespace(module="rh")
        navigator.open_module = lambda key: setattr(navigator, "module", key)

        navigation._navigator = navigator
        navigation._auth = SimpleNamespace(
            session=SimpleNamespace(authenticated=True),
        )
        navigation._registry = ModuleRegistry()

        definition = navigation._definition(
            navigation._registry.allowed({1, 3, 5, 6, 7}),
        )

        self.assertEqual(definition.key, "home")
        self.assertEqual(navigator.module, "home")

    def test_form_resources_remain_isolated_between_modules(self):
        registry = AssetRegistry(
            ExtrasAsset(editor=False),
        )

        self.assertEqual(
            registry.allowed(
                {1, 3, 5, 6, 7},
                authenticated=True,
            ),
            (),
        )

    def test_sidebar_index_uses_filtered_modules(self):
        registry = ModuleRegistry()
        modules = registry.allowed({1, 3, 5, 6, 7})

        self.assertEqual(registry.index("producao", modules), 1)
        self.assertEqual(registry.index("pcp", modules), 0)

    def test_assets_follow_form_resources(self):
        registry = AssetRegistry(
            PublicAsset(editor=False),
            ProtectedAsset(editor=False),
        )

        self.assertEqual(
            tuple(
                asset.definition.key
                for asset in registry.by_keys(
                    "public",
                    "protected",
                    resources={10},
                    authenticated=True,
                )
            ),
            ("protected",),
        )

        self.assertEqual(
            tuple(
                asset.definition.key
                for asset in registry.by_keys(
                    "public",
                    "protected",
                    resources=set(),
                    authenticated=False,
                )
            ),
            ("public",),
        )

    def test_pcp_form_uses_form_resource(self):
        self.assertEqual(BasePrecosAsset.DEFINITION.resource_id, 4)


if __name__ == "__main__":
    unittest.main()
