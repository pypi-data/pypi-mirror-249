import logging

import psycopg
from langchain.memory.entity import BaseEntityStore
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

DEFAULT_CONNECTION_STRING = "postgresql://postgres:mypassword@localhost/chat_history"


class JarvisEntityStore(BaseEntityStore):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "entity_store",
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
            entity_name VARCHAR(256),
            entity_discription TEXT "",
            session_id BIGINT
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()
