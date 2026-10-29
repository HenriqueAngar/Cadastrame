"""Teste completo com conta temporária no banco de desenvolvimento.
Habilite com CADASTRAME_ACCESS_DB_TESTS=1. Não executa em produção.
"""
import os
import unittest


@unittest.skipUnless(os.environ.get("CADASTRAME_ACCESS_DB_TESTS") == "1", "Integração de acesso: execução explícita")
class AccessControlIntegrationTests(unittest.TestCase):
    def test_login_roles_revocation_logout_and_expiration(self):
        import sys
        import uuid
        from datetime import datetime, timedelta
        from pathlib import Path

        import psycopg
        from streamlit.testing.v1 import AppTest

        root = Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(root))
        from infraesctruture.connection.config import Settings, Config, ConnectionType
        from infraesctruture.connection.manager import manager
        from infraesctruture.auth.security import Security
        from infraesctruture.auth.manager import AuthManager
        from infraesctruture.auth.utils.handler import PasswordAlreadySetError
        from shared.records import Records

        settings = Settings()
        assert settings.application.environment == "development"
        assert settings.database.default.value == "teste"
        config = Config.get(ConnectionType.DATABASE, settings.database.default)
        connection = psycopg.connect(host=config.host, port=config.port, dbname=config.database,
                                    user=config.user, password=config.password, autocommit=True)
        suffix = uuid.uuid4().hex[:10]
        email = f"audit-{suffix}@example.invalid"
        password = uuid.uuid4().hex
        password_hash = Security.hash_password(password)
        user_id = None
        role_id = -32000
        role_created = False

        def menus(app):
            return {button.key for button in app.button if button.key and button.key.startswith("home:")}

        def check(app):
            assert not app.exception, str(app.exception)
            assert not app.error, [error.value for error in app.error]

        def login(app):
            app.text_input[0].set_value(email)
            next(button for button in app.button if button.label == "Continuar").click().run()
            check(app)
            app.text_input[0].set_value(password)
            next(button for button in app.button if button.label == "Entrar").click().run()
            check(app)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM cadastrame.roles WHERE id=%s", (role_id,))
                assert cursor.fetchone() is None
                cursor.execute("INSERT INTO cadastrame.roles(id,name,is_manager,created_at) VALUES (%s,%s,false,CURRENT_TIMESTAMP)", (role_id, f"audit-{suffix}"))
                role_created = True
                cursor.execute("INSERT INTO cadastrame.rolespermissions(role_id,resource_id) VALUES (%s,1),(%s,8)", (role_id, role_id))
                cursor.execute("INSERT INTO cadastrame.users(idrole,username,email,password,active,created_at,updated_at) VALUES (1,%s,%s,%s,true,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP) RETURNING iduser", (f"audit-{suffix}", email, password_hash))
                user_id = cursor.fetchone()[0]

            app = AppTest.from_file(str(root / "app.py"), default_timeout=30).run()
            check(app)
            login(app)
            assert menus(app) == {"home:pcp", "home:producao", "home:rh"}
            assert not app.session_state["context"].data, "Credenciais permaneceram no contexto"
            print("OK: login real e acesso de administrador")

            for role, allowed, page in [(2, {"home:pcp"}, "pcp"),
                                        (3, {"home:producao"}, "producao"),
                                        (4, {"home:rh"}, "rh"),
                                        (5, {"home:producao"}, "producao")]:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM cadastrame.roles WHERE id=%s", (role,))
                    if cursor.fetchone() is None:
                        continue
                    cursor.execute("UPDATE cadastrame.users SET idrole=%s WHERE iduser=%s", (role, user_id))
                app.run()
                check(app)
                assert menus(app) == allowed, (role, menus(app))
                next(button for button in app.button if button.key == "home:" + page).click().run()
                check(app)
                assert app.session_state["module"] == page
                labels = [element.label for element in app.radio]
                print("OK: perfil", role, "menus", sorted(allowed), "módulo aberto", page)

            with connection.cursor() as cursor:
                cursor.execute("UPDATE cadastrame.users SET idrole=%s WHERE iduser=%s", (role_id, user_id))
            app.run()
            check(app)
            assert menus(app) == {"home:rh"}
            app.session_state["module"] = "pcp"
            app.run()
            check(app)
            assert app.session_state["module"] == "home"
            print("OK: navegação forçada para módulo não autorizado retorna à página inicial")

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM cadastrame.rolespermissions WHERE role_id=%s AND resource_id=8", (role_id,))
            app.run()
            check(app)
            assert menus(app) == set()
            print("OK: revogação no banco altera os menus sem novo login")

            with connection.cursor() as cursor:
                cursor.execute("UPDATE cadastrame.users SET active=false WHERE iduser=%s", (user_id,))
            app.run()
            check(app)
            assert not app.session_state["authenticated"]
            assert app.text_input[0].label == "E-mail"
            print("OK: conta desativada perde sessão na próxima interação")

            with connection.cursor() as cursor:
                cursor.execute("UPDATE cadastrame.users SET active=true,idrole=4 WHERE iduser=%s", (user_id,))
            login(app)
            assert menus(app) == {"home:rh"}
            next(button for button in app.button if button.key == "auth:logout").click().run()
            check(app)
            assert not app.session_state["authenticated"]
            assert app.session_state["records"].empty
            assert not app.session_state["context"].data
            print("OK: saída limpa sessão, formulários e pendentes")

            login(app)
            app.session_state["expires_at"] = datetime.now() - timedelta(seconds=1)
            app.run()
            check(app)
            assert not app.session_state["authenticated"]
            print("OK: sessão expirada não é renovada")

            try:
                AuthManager().create_password(email, "not-applied")
            except PasswordAlreadySetError:
                pass
            else:
                raise AssertionError("Primeiro acesso sobrescreveu senha existente")
            with connection.cursor() as cursor:
                cursor.execute("SELECT password FROM cadastrame.users WHERE iduser=%s", (user_id,))
                assert cursor.fetchone()[0] == password_hash
            print("OK: senha existente preservada no banco")
        finally:
            with connection.cursor() as cursor:
                if user_id is not None:
                    cursor.execute("DELETE FROM cadastrame.users WHERE iduser=%s AND email=%s", (user_id, email))
                if role_created:
                    cursor.execute("DELETE FROM cadastrame.rolespermissions WHERE role_id=%s", (role_id,))
                    cursor.execute("DELETE FROM cadastrame.roles WHERE id=%s AND name=%s", (role_id, f"audit-{suffix}"))
            connection.close()
            manager.shutdown()
            print("Conta e perfil temporários removidos do banco de teste.")
