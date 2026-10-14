from dataclasses import dataclass
from typing import Optional

import psycopg
from psycopg import sql


@dataclass
class ValidationResult:
    success: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None


class SQLValidator:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 5433,
        dbname: str = "migration_test",
        user: str = "postgres",
        password: str = "postgres",
    ):
        self.connection_config = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
            "connect_timeout": 5,
        }

    def validate(self, query: str) -> ValidationResult:
        if not query or not query.strip():
            return ValidationResult(
                success=False,
                error_type="EmptyQuery",
                error_message="SQL query is empty.",
            )

        try:
            with psycopg.connect(**self.connection_config) as conn:
                with conn.cursor() as cur:
                    # Read-only mode prevents writes in this transaction.
                    cur.execute("SET TRANSACTION READ ONLY")

                    # EXPLAIN checks query planning without running the
                    # SELECT itself or returning its result set.
                    cur.execute(
                        sql.SQL("EXPLAIN {}").format(sql.SQL(query))
                    )

                    cur.fetchall()

            return ValidationResult(success=True)

        except psycopg.Error as exc:
            return ValidationResult(
                success=False,
                error_type=type(exc).__name__,
                error_message=str(exc).strip(),
            )