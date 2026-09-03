"""Gerenciamento da sessão da aplicação."""

from __future__ import annotations

from datetime import datetime, timedelta

import streamlit as st

from infraesctruture.auth.utils.models import UserContext


class Session:

    def __init__(
        self,
        timeout_minutes: int = 10,
    ):

        self._timeout = timedelta(
            minutes=timeout_minutes
        )

        state = st.session_state

        state.setdefault(
            "authenticated",
            False,
        )

        state.setdefault(
            "user",
            None,
        )

        state.setdefault(
            "started_at",
            None,
        )

        state.setdefault(
            "expires_at",
            None,
        )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def authenticated(self) -> bool:

        return st.session_state.authenticated

    @property
    def user(self) -> UserContext | None:

        return st.session_state.user

    @property
    def expires_at(self) -> datetime | None:

        return st.session_state.expires_at

    # ==========================================================
    # LOGIN / LOGOUT
    # ==========================================================

    def login(
        self,
        user: UserContext,
    ) -> None:

        self.logout()

        now = datetime.now()

        st.session_state.user = user
        st.session_state.authenticated = True
        st.session_state.started_at = now
        st.session_state.expires_at = now + self._timeout

    def logout(self) -> None:

        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.started_at = None
        st.session_state.expires_at = None

    # ==========================================================
    # SESSION
    # ==========================================================

    def touch(self) -> None:

        if self.authenticated:

            st.session_state.expires_at = (
                datetime.now()
                + self._timeout
            )

    def expired(self) -> bool:

        if not self.authenticated:
            return True

        expires_at = st.session_state.expires_at

        if expires_at is None:

            self.logout()

            return True

        if datetime.now() >= expires_at:

            self.logout()

            return True

        return False

    def remaining(self) -> timedelta:

        if self.expired():
            return timedelta()

        return (
            st.session_state.expires_at
            - datetime.now()
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self) -> None:

        self.logout()