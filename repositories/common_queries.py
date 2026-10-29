
GET_IDPRODUTO = """
SELECT
    idproduto
FROM
    pdgeral.produtos
WHERE
    codproduto = %s
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

SEARCH_INPUT = """
SELECT
    {key_field} AS chavecampo,
    {code_field} AS codigocampo,
    {description_field} AS descricaocampo
FROM
    {table}
{where}
GROUP BY
    1, 2, 3
ORDER BY
    descricaocampo
"""