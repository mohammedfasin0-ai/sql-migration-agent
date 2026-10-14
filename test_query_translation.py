from pathlib import Path
import sqlglot
from sqlglot import exp

PROJECT_ROOT = Path(__file__).resolve().parent
query_path = (
    PROJECT_ROOT
    / "fixtures"
    / "legacy"
    / "customer_report.sql"
)

oracle_sql = query_path.read_text(encoding="utf-8")

tree = sqlglot.parse_one(oracle_sql, read="oracle")

for node in tree.find_all(exp.Sub):
    if (
        isinstance(node.this, exp.CurrentTimestamp)
        and node.this.args.get("sysdate")
        and isinstance(node.expression, exp.Literal)
        and node.expression.is_number
    ):
        days = node.expression.copy()

        interval = exp.Interval(
            this=days,
            unit=exp.Var(this="DAY"),
        )

        node.replace(
            exp.Sub(
                this=exp.CurrentTimestamp(),
                expression=interval,
            )
        )

translated_query = tree.sql(dialect="postgres")

print("SQLGlot PostgreSQL translation:")
print("=" * 50)
print(translated_query)