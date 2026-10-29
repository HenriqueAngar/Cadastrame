"""Consultas SQL do repositório de Produção."""

# ==========================================================
# ENSAQUES
# ==========================================================

GET_NEXT_IDENSAQUE = """
SELECT
    COALESCE(MAX(idensaque), 0) + 1
FROM
    srcproducao.cadensaques
"""


INSERT_ENSAQUE = """
INSERT INTO
    srcproducao.cadensaques
(
    idensaque,
    dataensaque,
    idop,
    idproduto,
    codop,
    codproduto,
    turno,
    linha,
    quantidade
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
"""


# ==========================================================
# PRODUÇÃO
# ==========================================================

GET_NEXT_IDOUTPUT = """
SELECT
    COALESCE(MAX(idoutput), 0) + 1
FROM
    srcproducao.cadoutput
"""


INSERT_OUTPUT = """
INSERT INTO
    srcproducao.cadoutput
(
    idoutput,
    dataentrada,
    idop,
    idproduto,
    codop,
    codproduto,
    turno,
    linha,
    producao,
    reprocesso,
    motivoreprocesso
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
"""


# ==========================================================
# PARADAS
# ==========================================================

GET_NEXT_IDPARADA = """
SELECT
    COALESCE(MAX(idparada), 0) + 1
FROM
    srcproducao.cadparadas
"""


INSERT_PARADA = """

INSERT INTO
    srcproducao.cadparadas
(
    datahorainicio,
    datahorafim,
    linha,
    tipoparada,
    motivoparada,
    observacao
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)

"""


GET_IDORDEMPRODUCAO = """
SELECT
    idordemproducao
FROM
    pdestoque.ordensproducao
WHERE
    codordemproducao = %s
"""