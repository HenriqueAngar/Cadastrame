"""Serviços de segurança e criptografia."""

from __future__ import annotations

import bcrypt


class Security:
    """
    Responsável pelas operações criptográficas da aplicação.
    """

    # ==========================================================
    # PASSWORD
    # ==========================================================

    @staticmethod
    def hash_password(
        password: str,
    ) -> str:

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify_password(
        password: str,
        password_hash: str,
    ) -> bool:

        if not password_hash:
            return False

        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )