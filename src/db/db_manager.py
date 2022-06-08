from typing import TYPE_CHECKING

import psycopg2

if TYPE_CHECKING:
    from psycopg2.extensions import connection as PostgreSQLConnection


class DBManager:
    def __init__(
        self, db_service_name: str, db_name: str, db_user: str, db_password: str
    ) -> None:
        self.__db_service_name = db_service_name
        self.__db_name = db_name
        self.__db_user = db_user
        self.__db_password = db_password

    def get_connection(self) -> "PostgreSQLConnection":
        psycopg2.connect(
            host=self.__db_service_name,
            database=self.__db_name,
            user=self.__db_user,
            password=self.__db_password,
        )
