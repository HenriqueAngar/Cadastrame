from __future__ import annotations

from contextlib import contextmanager

import pandas as pd

from psycopg import sql

from infraesctruture.connection.manager import manager

from repositories import common_queries as queries


class Repository:

    # ==========================================================
    # CONNECTION
    # ==========================================================

    @contextmanager
    def cursor(
        self,
    ):

        with manager.database() as conn:

            with conn.cursor() as cur:

                yield cur

    # ==========================================================
    # TABLE
    # ==========================================================

    def table(
        self,
        query: str | sql.Composable,
        params: tuple | None = None,
    ) -> pd.DataFrame:

        with self.cursor() as cur:

            cur.execute(

                query,

                params,

            )

            rows = cur.fetchall()

            columns = [

                column.name

                for column in cur.description

            ]

            return pd.DataFrame(

                rows,

                columns=columns,

            )

    # ==========================================================
    # SEARCH INPUT
    # ==========================================================

    def search_input(
        self,
        *,
        schema: str,
        table: str,
        key_field: str,
        description_field: str,
        code_field: str | None = None,
        params: dict | None = None,
    ) -> pd.DataFrame:

        code = (

            sql.Identifier(
                code_field,
            )

            if code_field is not None

            else sql.SQL(
                "NULL"
            )

        )

        where, values = self._search_where(

            params,

        )

        query = sql.SQL(

            queries.SEARCH_INPUT

        ).format(

            key_field=sql.Identifier(
                key_field,
            ),

            code_field=code,

            description_field=sql.Identifier(
                description_field,
            ),

            table=sql.Identifier(
                schema,
                table,
            ),

            where=where,

        )

        return self.table(

            query,

            values,

        )

    # ==========================================================
    # SEARCH WHERE
    # ==========================================================

    @staticmethod
    def _search_where(
        params: dict | None,
    ) -> tuple[
        sql.Composable,
        tuple,
    ]:

        if not params:

            return (

                sql.SQL(""),

                (),

            )

        conditions = []

        values = []

        for field, value in params.items():

            # ==================================================
            # NULL
            # ==================================================

            if value is None:

                conditions.append(

                    sql.SQL(
                        "{} IS NULL"
                    ).format(

                        sql.Identifier(
                            field,
                        )

                    )

                )

                continue

            # ==================================================
            # IN
            # ==================================================

            if isinstance(

                value,

                (
                    list,
                    tuple,
                    set,
                ),

            ):

                items = list(value)

                if not items:

                    conditions.append(

                        sql.SQL(
                            "FALSE"
                        )

                    )

                    continue

                placeholders = sql.SQL(
                    ", "
                ).join(

                    sql.Placeholder()

                    for _ in items

                )

                conditions.append(

                    sql.SQL(
                        "{} IN ({})"
                    ).format(

                        sql.Identifier(
                            field,
                        ),

                        placeholders,

                    )

                )

                values.extend(
                    items
                )

                continue

            # ==================================================
            # EQUAL
            # ==================================================

            conditions.append(

                sql.SQL(
                    "{} = %s"
                ).format(

                    sql.Identifier(
                        field,
                    )

                )

            )

            values.append(
                value
            )

        where = sql.SQL(
            "WHERE "
        ) + sql.SQL(
            "\nAND "
        ).join(
            conditions
        )

        return (

            where,

            tuple(values),

        )

    # ==========================================================
    # COMMON LISTS
    # ==========================================================

    def list_centros_custo(
        self,
    ) -> pd.DataFrame:

        return self.table(

            queries.LISTAR_CENTROS_CUSTO,

        )

    # ==========================================================
    # COMMON FIND
    # ==========================================================

    def find_idproduto(
        self,
        codproduto: int,
    ) -> int | None:

        with self.cursor() as cur:

            cur.execute(

                queries.GET_IDPRODUTO,

                (codproduto,),

            )

            row = cur.fetchone()

            return (

                None

                if row is None

                else row[0]

            )