"""Consultas SQL do repositório de custos de produtos."""

GET_IDPRODUTO = """
SELECT
    idproduto
FROM
    pdgeral.produtos
WHERE
    codproduto = %s
"""


GET_NEXT_IDPRECOREF = """
SELECT
    COALESCE(MAX(idprecoref), 0) + 1
FROM
    srccompras.baseprecos
"""


LISTAR_CENTROS_CUSTO = """
SELECT
    idcentrocusto,
    codcentrocusto,
    centrocusto
FROM
    pdgeral.centroscustos
ORDER BY
    centrocusto
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