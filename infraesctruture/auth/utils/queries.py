"""Consultas SQL da autenticação."""

# ==========================================================
# SELECT
# ==========================================================

GET_USER_BY_EMAIL = """
SELECT
    iduser,
    idrole,
    active,
    username,
    email,
    password,
    created_at,
    updated_at,
    deactivated_at
FROM cadastrame.users
WHERE lower(email) = lower(%s) and active is true;
"""


# ==========================================================
# UPDATE
# ==========================================================

UPDATE_PASSWORD = """
UPDATE cadastrame.users
SET
    password = %s,
    updated_at = CURRENT_TIMESTAMP
WHERE iduser = %s;
"""


UPDATE_LAST_LOGIN = """
UPDATE cadastrame.users
SET
    updated_at = CURRENT_TIMESTAMP
WHERE iduser = %s;
"""


ACTIVATE_USER = """
UPDATE cadastrame.users
SET
    active = TRUE,
    updated_at = CURRENT_TIMESTAMP,
    deactivated_at = TIMESTAMPTZ '2999-12-31 23:59:59'
WHERE iduser = %s;
"""


DEACTIVATE_USER = """
UPDATE cadastrame.users
SET
    active = FALSE,
    updated_at = CURRENT_TIMESTAMP,
    deactivated_at = CURRENT_TIMESTAMP
WHERE iduser = %s;
"""


UPDATE_EMAIL = """
UPDATE cadastrame.users
SET
    email = %s,
    updated_at = CURRENT_TIMESTAMP
WHERE iduser = %s;
"""


UPDATE_USERNAME = """
UPDATE cadastrame.users
SET
    username = %s,
    updated_at = CURRENT_TIMESTAMP
WHERE iduser = %s;
"""

GET_ROLE_RESOURCES = """
SELECT
    r.id,
    r.page_code,
    r.form_code,
    r.description
FROM cadastrame.resources r
INNER JOIN cadastrame.rolespermissions rp
    ON rp.resource_id = r.id
WHERE rp.role_id = %s
ORDER BY
    r.page_code,
    r.form_code;
"""