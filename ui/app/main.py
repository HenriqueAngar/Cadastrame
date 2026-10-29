"""Inicialização da aplicação."""

from __future__ import annotations

import streamlit as st

from ui.app.navigation import Navigation


def main():

    st.set_page_config(
        page_title="Cadastra.me",
        page_icon="📥",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    Navigation().run()


if __name__ == "__main__":

    main()