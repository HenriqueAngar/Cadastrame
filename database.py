import psycopg2
import streamlit as st


def conectar_banco():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )


def buscar_usuario_por_email(email):
    conn = conectar_banco()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                iduser,
                idrole,
                active,
                username,
                email
            FROM users
            WHERE LOWER(email) = LOWER(%s)
            LIMIT 1;
            """,
            (email.strip(),)
        )

        usuario = cursor.fetchone()

        cursor.close()

        return usuario

    finally:
        conn.close()