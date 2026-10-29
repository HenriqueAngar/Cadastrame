"""Consultas SQL do repositório de custos de produtos."""


GET_NEXT_IDPRECOREF = """
SELECT
    COALESCE(MAX(idprecoref), 0) + 1
FROM
    srccompras.baseprecos
"""


DELETE_PERIODO = """
DELETE FROM
    srccompras.baseprecos
WHERE
    idproduto = %s
    AND datainicio = %s
    AND datafim = %s
"""


INSERT = """
INSERT INTO
    srccompras.baseprecos
(
    idprecoref,
    idproduto,
    datainicio,
    datafim,
    preco
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s
)
"""