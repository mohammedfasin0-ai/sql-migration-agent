import re


def prune_schema(schema_sql: str, table_names: set[str]) -> str:
    relevant_tables = []

    for match in re.finditer(
        r"CREATE\s+TABLE\s+(\w+)\s*\(.*?\);",
        schema_sql,
        re.IGNORECASE | re.DOTALL,
    ):
        table_name = match.group(1)

        if table_name.lower() in {name.lower() for name in table_names}:
            relevant_tables.append(match.group(0))

    return "\n\n".join(relevant_tables)