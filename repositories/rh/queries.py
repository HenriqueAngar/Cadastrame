"""Consultas SQL do cadastro manual de extras de folha."""

# A folha processada delimita a empresa/unidade atendida pelos extras.
# idpessoa pode se repetir em empresas distintas no cadastro de colaboradores.
LIST_COLABORADORES_EXTRAS = """
SELECT c.idpessoa, MIN(c.nome) AS nome
FROM srcrh.colaboradores c
WHERE c.ativo = 1
  AND EXISTS (
      SELECT 1 FROM pdrh.folhas f
      WHERE f.idpessoa = c.idpessoa
        AND f.idempresa = c.idempresa
        AND f.idextra IS NULL
  )
GROUP BY c.idpessoa
HAVING COUNT(DISTINCT c.nome) = 1
ORDER BY nome, c.idpessoa
"""


FIND_IDCOLABORADOR = """
SELECT
    MIN(c.idpessoa) AS idcolaborador
FROM
    srcrh.colaboradores c
WHERE
    c.idpessoa = %s
    AND c.ativo = 1
    AND EXISTS (
        SELECT 1 FROM pdrh.folhas f
        WHERE f.idpessoa = c.idpessoa
          AND f.idempresa = c.idempresa
          AND f.idextra IS NULL
    )
HAVING COUNT(DISTINCT c.nome) = 1
"""


# Considera apenas a folha do ERP, sem os extras manuais já lançados.
FIND_CENTROS_COLABORADOR = """
SELECT DISTINCT
    f.idcentrocusto,
    cc.codcentrocusto
FROM pdrh.folhas f
LEFT JOIN pdgeral.centroscustos cc
    ON cc.idcentrocusto = f.idcentrocusto
WHERE f.idpessoa = %s
  AND f.competencia = %s
  AND f.idextra IS NULL
ORDER BY f.idcentrocusto NULLS LAST, cc.codcentrocusto
"""


UPSERT_EXTRA = """
INSERT INTO srcrh.cadextras
(
    idcolaborador,
    idcentrocusto,
    codigocentrocusto,
    competencia,
    horasextras,
    valoresextras,
    observacao
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT (
    idcolaborador,
    (COALESCE(codigocolaborador, '-1'::bigint)),
    (COALESCE(codigocentrocusto, -1)),
    competencia
) DO UPDATE SET
    idcolaborador = EXCLUDED.idcolaborador,
    idcentrocusto = EXCLUDED.idcentrocusto,
    codigocentrocusto = EXCLUDED.codigocentrocusto,
    competencia = EXCLUDED.competencia,
    horasextras = EXCLUDED.horasextras,
    valoresextras = EXCLUDED.valoresextras,
    observacao = EXCLUDED.observacao
"""
