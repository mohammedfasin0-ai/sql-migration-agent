import os

from dotenv import load_dotenv
from groq import Groq

from migration_task import MigrationTask


load_dotenv()


class LLMTranslator:

    def __init__(self):
        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

    def translate(self, task: MigrationTask) -> str:

        prompt = f"""
Convert the following SQL from Oracle to PostgreSQL.

Source dialect: {task.source_dialect}
Target dialect: {task.target_dialect}

Relevant database schema:
{task.relevant_schema}

Original SQL:
{task.original_sql}

Return only the converted PostgreSQL SQL.
Do not explain your answer.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert database migration engineer. "
                        "Convert Oracle SQL to PostgreSQL accurately."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content