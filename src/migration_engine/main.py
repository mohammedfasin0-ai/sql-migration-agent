from pathlib import Path

from sql_parser import extract_tables
from schema_pruner import prune_schema
from migration_task import MigrationTask
from llm_translator import LLMTranslator
from sql_validator import SQLValidator

PROJECT_ROOT = Path(__file__).resolve().parent[2]

query_path = PROJECT_ROOT / "fixtures" / "legacy" / "customer_report.sql"
schema_path = PROJECT_ROOT / "fixtures" / "schema" / "legacy_schema.sql"

sql = query_path.read_text()
schema_sql = schema_path.read_text()

tables = extract_tables(sql)
relevant_schema = prune_schema(schema_sql, tables)

task = MigrationTask(
    original_sql=sql,
    source_dialect="oracle",
    target_dialect="postgres",
    relevant_schema=relevant_schema,
)

print("Migration Task")
print("=" * 50)

print(f"Source dialect: {task.source_dialect}")
print(f"Target dialect: {task.target_dialect}")

print("\nOriginal SQL:")
print(task.original_sql)

print("\nRelevant schema:")
print(task.relevant_schema)

translator = LLMTranslator()

translated_sql = translator.translate(task)

print("\nTranslated PostgreSQL SQL:")
print(translated_sql)

validator = SQLValidator()
result = validator.validate(translated_sql)

print("\nValidation Result")
print("=" * 50)
print(f"Success: {result.success}")

if not result.success:
    print(f"Error type: {result.error_type}")
    print(f"Error message: {result.error_message}")