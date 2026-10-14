from pathlib import Path

from src.migration_engine.schema_translator import translate_schema

PROJECT_ROOT = Path(__file__).resolve().parent

schema_path = (
    PROJECT_ROOT
    / "fixtures"
    / "schema"
    / "legacy_schema.sql"
)

schema_sql = schema_path.read_text(encoding="utf-8")

translated_schema = translate_schema(schema_sql)

print("Translated PostgreSQL schema:")
print("=" * 50)
print(translated_schema)