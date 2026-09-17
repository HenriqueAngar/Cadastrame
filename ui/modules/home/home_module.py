"""Módulo Home, ponto exclusivo de entrada da aplicação."""

from __future__ import annotations

import streamlit as st


class HomeModule:
    """Apresenta a entrada do usuário para os módulos de negócio."""

    def respond(self) -> str | None:
        st.title("🏠 Home")
        st.subheader("Bem-vindo ao Cadastrame")
        st.write("Escolha uma área para iniciar o trabalho.")

        left, right = st.columns(2)

        with left:
            if st.button("🗂️ Cadastros", use_container_width=True):
                return "cadastros"

        with right:
            if st.button("⚙️ Operações", use_container_width=True):
                return "operacoes"

        st.info(
            "A autenticação, os casos de uso e as regras de negócio serão "
            "conectados nas próximas etapas."
        )
        return None

