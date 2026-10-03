from pydantic import BaseModel


class MigrationTask(BaseModel):
    original_sql: str
    source_dialect: str
    target_dialect: str
    relevant_schema: str