import sqlglot


def translate_schema(
    schema_sql: str,
    source_dialect: str = "oracle",
    target_dialect: str = "postgres",
) -> str:
    statements = sqlglot.parse(
        schema_sql,
        read=source_dialect,
    )

    translated_statements = []

    for statement in statements:
        if statement is None:
            continue

        translated_statements.append(
            statement.sql(dialect=target_dialect)
        )

    return ";\n\n".join(translated_statements) + ";"