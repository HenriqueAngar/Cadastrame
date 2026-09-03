"""Gerenciador da autenticação."""

from __future__ import annotations

from infraesctruture.auth.provider import AuthProvider
from infraesctruture.auth.security import Security
from infraesctruture.auth.session import Session

from infraesctruture.auth.utils.models import (
    Resource,
    UserContext,
    UserRecord,
)

from infraesctruture.auth.utils.handler import (
    AuthenticationStatus,
    InactiveUserError,
    InvalidPasswordError,
    UserNotFoundError,
)


class AuthManager:

    def __init__(self):

        self._provider = AuthProvider()
        self._session = Session()

    # ==========================================================
    # LOGIN
    # ==========================================================

    def login(
        self,
        email: str,
        password: str,
    ) -> AuthenticationStatus:

        user = self._get_user(
            email,
        )

        if not Security.verify_password(
            password,
            user.password,
        ):
            raise InvalidPasswordError()

        self._start_session(
            user,
        )

        self._provider.update_last_login(
            user.iduser,
        )

        return AuthenticationStatus.AUTHENTICATED

    # ==========================================================
    # CREATE PASSWORD
    # ==========================================================

    def create_password(
        self,
        email: str,
        password: str,
    ) -> AuthenticationStatus:

        user = self._get_user(
            email,
        )

        password_hash = Security.hash_password(
            password,
        )

        self._provider.update_password(
            user.iduser,
            password_hash,
        )

        self._start_session(
            user,
        )

        return AuthenticationStatus.AUTHENTICATED

    # ==========================================================
    # LOGOUT
    # ==========================================================

    def logout(self) -> None:

        self._session.logout()

    # ==========================================================
    # SESSION
    # ==========================================================

    @property
    def session(self) -> Session:

        return self._session

    # ==========================================================
    # IDENTIFY
    # ==========================================================

    def identify(
        self,
        email: str,
    ) -> AuthenticationStatus:

        user = self._provider.get_user_by_email(
            email,
        )

        if user is None:
            return AuthenticationStatus.USER_NOT_FOUND

        if not user.active:
            raise InactiveUserError()

        if user.password is None:
            return AuthenticationStatus.FIRST_ACCESS

        return AuthenticationStatus.PASSWORD_REQUIRED

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _get_user(
        self,
        email: str,
    ) -> UserRecord:

        user = self._provider.get_user_by_email(
            email,
        )

        if user is None:
            raise UserNotFoundError()

        if not user.active:
            raise InactiveUserError()

        return user

    def _start_session(
        self,
        user: UserRecord,
    ) -> None:

        resources = self._provider.get_role_resources(
            user.idrole,
        )

        self._session.login(
            self._context(
                user,
                resources,
            ),
        )

    @staticmethod
    def _context(
        user: UserRecord,
        resources: list[Resource],
    ) -> UserContext:

        return UserContext(
            iduser=user.iduser,
            idrole=user.idrole,
            username=user.username,
            email=user.email,
            resources=resources,
        )