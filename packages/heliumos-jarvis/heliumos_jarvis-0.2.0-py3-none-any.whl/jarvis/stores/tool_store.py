import json
import logging
from abc import ABC
from typing import (
    Optional, Dict
)

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from pydantic import BaseModel

logger = logging.getLogger(__name__)
DEFAULT_CONNECTION_STRING = "postgresql://postgres:mypassword@localhost/q_xun"


class Tool(BaseModel):
    id: str
    tool_name: str
    tool_description: str
    tool_type: str


class ToolInstance(BaseModel):
    id: str
    tool_id: str
    tool_name: str
    tool_type: str
    instance_parameters: Optional[Dict] = None


class ToolStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "tools",
    ):
        try:
            self.connection = psycopg.connect(connection_string)
            self.cursor = self.connection.cursor(row_factory=dict_row)
        except psycopg.OperationalError as error:
            logger.error(error)
        self.table_name = table_name
        self._create_table_if_not_exists()
        self._insert_tools_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGINT PRIMARY KEY,
            tool_name VARCHAR(256),
            tool_type VARCHAR(256),
            tool_description TEXT NOT NULL
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def _insert_tools_if_not_exists(self) -> None:
        query = sql.SQL(f"INSERT INTO {self.table_name} (id, tool_name, tool_type, tool_description) "
                        f"select %s, %s, %s, %s WHERE NOT EXISTS (SELECT id from {self.table_name} where id = %s )")

        print(query)
        self.cursor.execute(
            query, ("1", "CALCULATOR", "BUILD_IN", "TT", "1")
        )
        self.cursor.execute(
            query, ("2", "RETRIEVE", "BUILD_IN", "TT", "2")
        )
        self.cursor.execute(
            query, ("3", "TRANSLATOR", "BUILD_IN", "TT", "3")
        )
        self.connection.commit()

    def get_tools(self):
        query = (
            f"SELECT * FROM {self.table_name} ORDER by id;"
        )
        self.cursor.execute(query, ())
        records = self.cursor.fetchall()

        return [Tool(
            id=str(record["id"]),
            tool_name=record["tool_name"],
            tool_type=record["tool_type"],
            tool_description=record["tool_description"]
        ) for record in records]

    def get_tool_by_id(self, tool_id):
        query = (
            f"SELECT * FROM {self.table_name} WHERE id = %s ORDER by id limit 1 ;"
        )
        self.cursor.execute(query, (tool_id,))
        records = self.cursor.fetchall()
        return Tool(
            id=str(records[0]["id"]),
            tool_name=records[0]["tool_name"],
            tool_type=records[0]["tool_type"],
            tool_description=records[0]["tool_description"]
        )


class ToolInstanceStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "tool_instances",
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
            tool_id BIGINT,
            instance_parameters TEXT
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def get_instance_by_id(self, instance_id: str) -> ToolInstance:
        query = (
            f"SELECT {self.table_name}.id AS id, "
            f"{self.table_name}.tool_id AS tool_id, "
            f"tools.tool_name  AS tool_name, "
            f"tools.tool_type AS tool_type, "
            f"{self.table_name}.instance_parameters AS instance_parameters "
            f" FROM {self.table_name} LEFT JOIN tools ON  {self.table_name}.tool_id = tools.id WHERE {self.table_name}.id = %s ORDER by {self.table_name}.id limit 1 ;"
        )
        self.cursor.execute(query, (instance_id,))
        records = self.cursor.fetchall()
        instance_dict = records[0]
        instance = ToolInstance(
            id=str(instance_dict["id"]),
            tool_id=str(instance_dict["tool_id"]),
            tool_name=instance_dict["tool_name"],
            tool_type=instance_dict["tool_type"],
            instance_parameters=json.loads(instance_dict["instance_parameters"])
        )
        return instance

    def add_tool_instance(
            self,
            instance_id: str,
            tool_id: str,
            instance_parameters: str
    ):

        query = (sql.SQL("INSERT INTO {} (id, tool_id, instance_parameters) VALUES (%s, %s, %s);")
                 .format(sql.Identifier(self.table_name)))
        self.cursor.execute(
            query, (instance_id, tool_id, instance_parameters)
        )
        self.connection.commit()

    def get_instances(self):
        query = (
            f"SELECT {self.table_name}.id AS id, "
            f"{self.table_name}.tool_id AS tool_id, "
            f"tools.tool_name  AS tool_name, "
            f"tools.tool_type AS tool_type, "
            f"{self.table_name}.instance_parameters AS instance_parameters "
            f" FROM {self.table_name} LEFT JOIN tools ON  {self.table_name}.tool_id = tools.id ORDER by {self.table_name}.id;"
        )
        self.cursor.execute(query, ())
        records = self.cursor.fetchall()
        instances = [ToolInstance(
            id=str(instance_dict["id"]),
            tool_id=str(instance_dict["tool_id"]),
            tool_name=instance_dict["tool_name"],
            tool_type=instance_dict["tool_type"],
            instance_parameters=json.loads(instance_dict["instance_parameters"])
        ) for instance_dict in records]
        return instances
