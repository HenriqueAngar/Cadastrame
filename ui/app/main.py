"""Inicialização da aplicação Streamlit."""

from __future__ import annotations

import streamlit as st

from ui.app.navigation import Navigation


def main() -> None:
    """Configura a aplicação e inicia a navegação principal."""

    st.set_page_config(
        page_title="Cadastrame",
        page_icon="📥",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    Navigation().run()

