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
    AccessDeniedError,
    PasswordAlreadySetError,
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

        if user.password is not None:
            raise PasswordAlreadySetError()
        if not password or not password.strip():
            raise InvalidPasswordError()

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

    def refresh(self) -> bool:
        """Revalida conta e permissões no banco, sem renovar sessão expirada."""
        if not self._session.authenticated or self._session.expired():
            return False
        try:
            user = self._provider.get_user_by_id(self._session.user.iduser)
            if user is None or not user.active:
                self._session.logout()
                return False
            resources = self._provider.get_role_resources(user.idrole)
            self._session.update_user(self._context(user, resources))
            return True
        except Exception:
            self._session.logout()
            raise

    def require_resource(self, page_code: str, form_code: str) -> UserContext:
        if not self.refresh():
            raise AccessDeniedError()
        user = self._session.user
        if not any(r.page_code == page_code and r.form_code == form_code for r in user.resources):
            raise AccessDeniedError()
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
            resources=tuple(resources),
        )