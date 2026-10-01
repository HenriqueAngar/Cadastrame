import streamlit as st
import psycopg2


# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="Cadastrame",
    layout="centered"
)


# ==========================================
# CONEXÃO COM O BANCO
# ==========================================

def conectar_banco():

    return psycopg2.connect(
        host="192.168.56.101",
        port=5432,
        database="teste",
        user="rique",
        password="B2GripenNGKc390F4"
    )


# ==========================================
# VERIFICAR E-MAIL
# ==========================================

def verificar_email(email):

    conn = conectar_banco()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                iduser,
                username,
                email,
                active
            FROM cadastrame.users
            WHERE LOWER(TRIM(email)) = LOWER(TRIM(%s))
            LIMIT 1;
            """,
            (email,)
        )

        usuario = cursor.fetchone()

        cursor.close()

        return usuario

    finally:

        conn.close()


# ==========================================
# CSS
# ==========================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 450px;
        padding-top: 80px;
    }

    .logo {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 55px;
    }

    .titulo {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# MARCA
# ==========================================

st.markdown(
    """
    <div class="logo">
        Cadastrame
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# TÍTULO
# ==========================================

st.markdown(
    """
    <div class="titulo">
        Entrar
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# E-MAIL
# ==========================================

email = st.text_input(
    "E-mail",
    placeholder="Digite seu e-mail"
)


# ==========================================
# CONTINUAR
# ==========================================

if st.button(
    "Continuar",
    type="primary",
    use_container_width=True
):

    if not email.strip():

        st.error("Digite seu e-mail.")

    else:

        try:

            usuario = verificar_email(email)

            # ==================================
            # E-MAIL NÃO EXISTE NO BANCO
            # ==================================

            if usuario is None:

                st.error(
                    "Este e-mail não possui acesso ao Cadastrame."
                )

            # ==================================
            # USUÁRIO DESATIVADO
            # ==================================

            elif not usuario[3]:

                st.error(
                    "Este usuário está desativado."
                )

            # ==================================
            # USUÁRIO ENCONTRADO
            # ==================================

            else:

                st.success(
                    f"Bem-vindo, {usuario[1]}!"
                )

        except psycopg2.Error as erro:

            st.error(
                "Não foi possível conectar ao banco de dados."
            )

            st.exception(erro)