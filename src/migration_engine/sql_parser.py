import sqlglot
from sqlglot import exp

def extract_tables(sql: str) -> set[str]:

    tree = sqlglot.parse_one(sql,read="oracle")

    tables= {
        table.name for table in tree.find_all(exp.Table)
    }

    return tables