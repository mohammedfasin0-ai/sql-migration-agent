from dataclasses import dataclass
from uuid import UUID, uuid4

import psycopg
import sqlglot
from psycopg import sql

from src.migration_engine.schema_translator import translate_schema


@dataclass
class ProvisioningResult:
    run_id: str
    schema_name: str
    success: bool
    tables: list[str]
    error: str | None = None


def provision_schema(
    oracle_schema: str,
    db_config: dict,
) -> ProvisioningResult:
    # 1. Give this migration run a unique ID.
    run_id = str(uuid4())
    schema_name = f"migration_{run_id.replace('-', '')}"

    try:
        # 2. Translate Oracle DDL into PostgreSQL DDL.
        postgres_ddl = translate_schema(
            oracle_schema,
            source_dialect="oracle",
            target_dialect="postgres",
        )

        # 3. Parse the DDL into individual statements.
        statements = sqlglot.parse(postgres_ddl, read="postgres")
        statements = [stmt for stmt in statements if stmt is not None]

        if not statements:
            raise ValueError("No DDL statements were produced.")

        # Initial scope: only CREATE TABLE statements are allowed.
        for stmt in statements:
            if not isinstance(stmt, sqlglot.exp.Create):
                raise ValueError(
                    f"Unsupported DDL statement: {stmt.key}"
                )

            kind = stmt.args.get("kind")
            if str(kind).upper() != "TABLE":
                raise ValueError(
                    f"Unsupported CREATE object: {kind}"
                )

        # 4. Create the isolated schema and provision its tables.
        tables = []

        with psycopg.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("CREATE SCHEMA {}").format(
                        sql.Identifier(schema_name)
                    )
                )

                cur.execute(
                    sql.SQL("SET LOCAL search_path TO {}").format(
                        sql.Identifier(schema_name)
                    )
                )

                for index, statement in enumerate(statements, start=1):
                    cur.execute(statement.sql(dialect="postgres"))

                    table = statement.this

                    if isinstance(table, sqlglot.exp.Schema):
                        table = table.this

                        table_name = table.name
                        tables.append(table_name)

                        print(
                        f"[SUCCESS] Statement {index}: "
                        f"created {table_name}"
                    )

        # The connection context commits when it exits successfully.
        return ProvisioningResult(
            run_id=run_id,
            schema_name=schema_name,
            success=True,
            tables=tables,
        )

    except Exception as exc:
        # On failure, the connection context rolls back its transaction.
        return ProvisioningResult(
            run_id=run_id,
            schema_name=schema_name,
            success=False,
            tables=[],
            error=f"{type(exc).name}: {exc}",
        )