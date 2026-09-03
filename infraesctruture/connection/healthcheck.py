"""Health Check da infraestrutura de conexões."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

from infraesctruture.connection.config import Connection
from infraesctruture.connection.manager import manager


# ==========================================================
# DATABASE
# ==========================================================

def test_database():

    print(f"Conexão...: {Connection.TST.name}")

    with manager.database(Connection.TST) as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    current_database(),
                    current_user,
                    current_timestamp
            """)

            database, user, now = cur.fetchone()

            print(f"Banco......: {database}")
            print(f"Usuário....: {user}")
            print(f"Servidor...: {now}")

            cur.execute("""
                SELECT COUNT(*)
                FROM information_schema.schemata
            """)

            schemas = cur.fetchone()[0]

            print(f"Schemas....: {schemas}")


# ==========================================================
# REPOSITORY
# ==========================================================

def test_repository():

    print(f"Conexão...: {Connection.NFES.name}")

    repo = manager.repository(Connection.NFES)

    folder = Path(repo.share) / repo.path

    if not folder.exists():
        raise FileNotFoundError(folder)

    if not folder.is_dir():
        raise NotADirectoryError(folder)

    print(f"Repositório: {folder}")


# ==========================================================
# API
# ==========================================================

def test_api():

    print(f"Conexão...: {Connection.METEO.name}")

    session = manager.api(Connection.METEO)

    response = session.get(
        session.connection_config.base_url + "/v1/forecast",
        params={
            "latitude": -29.33,
            "longitude": -49.81,
            "current_weather": True,
        },
        timeout=30,
    )

    response.raise_for_status()

    weather = response.json()["current_weather"]

    print(f"Temperatura: {weather['temperature']} °C")
    print(f"Vento......: {weather['windspeed']} km/h")


# ==========================================================
# MANAGER
# ==========================================================

def test_manager():

    print("\n==============================")
    print("MANAGER")
    print("==============================")

    health = manager.health()

    print("\nResumo")

    print(f"Databases....: {len(health['databases'])}")
    print(f"APIs.........: {len(health['apis'])}")
    print(f"Repositories.: {len(health['repositories'])}")

    for resource_type, resources in health.items():

        print(f"\n{resource_type.upper()}")

        if not resources:

            print("  Nenhum recurso ativo.")
            continue

        for name, info in resources.items():

            print(f"\n  {name}")
            print(f"    Status......: {info['status']}")
            print(f"    Último uso..: {info['last_used']}")
            print(f"    Ocioso......: {info['idle_seconds']} s")


# ==========================================================
# RUNNER
# ==========================================================

def run_test(name: str, fn):

    print("\n==============================")
    print(name)
    print("==============================")

    start = perf_counter()

    try:

        fn()

        elapsed = (perf_counter() - start) * 1000

        print(f"Tempo.......: {elapsed:.0f} ms")
        print("Status......: OK")

    except Exception as ex:

        elapsed = (perf_counter() - start) * 1000

        print(f"Tempo.......: {elapsed:.0f} ms")
        print("Status......: ERRO")
        print(ex)


# ==========================================================
# PUBLIC
# ==========================================================

def run():

    try:

        run_test("DATABASE", test_database)

        run_test("REPOSITORY", test_repository)

        run_test("API", test_api)

        test_manager()

    finally:

        # Libera todos os recursos mesmo em caso de erro
        manager.shutdown()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    run()