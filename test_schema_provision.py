from pathlib import Path

from src.migration_engine.schema_provisioner import provision_schema

PROJECT_ROOT = Path(__file__).resolve().parent

schema_path = (
    PROJECT_ROOT / "fixtures" / "schema" / "legacy_schema.sql"
)

oracle_schema = schema_path.read_text(encoding="utf-8")

db_config = {
    "host": "127.0.0.1",
    "port": 5433,
    "dbname": "migration_test",
    "user": "postgres",
    "password": "postgres",
    "connect_timeout": 5,
}

result = provision_schema(oracle_schema, db_config)

print(f"\nRun ID: {result.run_id}")
print(f"Schema: {result.schema_name}")
print(f"Success: {result.success}")

if result.success:
    print("Tables:", result.tables)
else:
    print("Error:", result.error)