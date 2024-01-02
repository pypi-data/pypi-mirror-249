import logging
from abc import ABC

import psycopg
from psycopg.rows import dict_row
from pydantic import BaseModel

logger = logging.getLogger(__name__)
DEFAULT_CONNECTION_STRING = "postgresql://postgres:mypassword@localhost/q_xun"


class AgentProfile(BaseModel):
    knowledge_id: str
    id: str
    source_path: str
    source_summary: str


class AgentProfileStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "agent_profile",
    ):
        try:
            self.connection = psycopg.connect(connection_string)
            self.cursor = self.connection.cursor(row_factory=dict_row)
        except psycopg.OperationalError as error:
            logger.error(error)

        self.table_name = table_name

        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGINT PRIMARY KEY,
            profile_name VARCHAR(22),
            profile_description TEXT NOT NULL
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()
