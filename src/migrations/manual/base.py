from urllib.parse import urlparse, unquote

import asyncpg


class BaseMigration:
    """
    Base class for migrations

    For cases to run migrations manually because `aerich/tortoise-orm` doesn't allow to run migrations manually

    """

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None

    @staticmethod
    def prepare_connection_args(url: str):
        result = urlparse(url)
        if result.scheme != "postgres":
            raise ValueError(
                f"URL should start with 'postgres://', but got '{result.scheme}'"
            )

        db_user = result.username
        db_password = unquote(result.password) if result.password else None
        db_host = result.hostname
        db_port = result.port
        db_name = result.path.lstrip("/")  # Remove leading '/' from the path

        return dict(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )

    async def _connect(self) -> None:
        """
        Connect to the database

        Returns: None
        """
        self.conn = await asyncpg.connect(**self.prepare_connection_args(self.db_url))

    async def _close(self) -> None:
        """
        Close the connection to the database

        Returns: None

        """
        await self.conn.close()

    async def run(self) -> None:
        """
        Run the migration

        Returns: None

        """
        await self._connect()
        await self.apply()
        await self._close()

    async def execute(self, query: str) -> None:
        """
        Execute a query

        Args:
            query: str: Query to execute

        Returns: None

        """
        await self.conn.execute(query)

    async def apply(self) -> None:
        """
        Apply the migration

        Returns: None

        """
        raise NotImplementedError("Subclasses should implement this method")
