from datetime import datetime
from database.database import Database
from models.journal_entry import JournalEntry


class JournalRepository:
    """
    Handles storage and retrieval of Atlas trade journal entries.
    """

    def __init__(self, database: Database):
        self.database = database
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,

            entry_price REAL NOT NULL,
            exit_price REAL,

            score INTEGER,
            confidence REAL,

            trend TEXT,
            momentum TEXT,
            volatility TEXT,
            volume TEXT,

            market_condition TEXT,

            outcome TEXT,
            profit_loss REAL,

            notes TEXT,

            created TEXT
        )
        """

        self.database.connection.execute(query)
        self.database.connection.commit()


    def add(self, entry: JournalEntry):
        query = """
        INSERT INTO journal (
            symbol,
            direction,
            entry_price,
            exit_price,
            score,
            confidence,
            trend,
            momentum,
            volatility,
            volume,
            market_condition,
            outcome,
            profit_loss,
            notes,
            created
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            entry.symbol,
            entry.direction,
            entry.entry_price,
            entry.exit_price,
            entry.score,
            entry.confidence,
            entry.trend,
            entry.momentum,
            entry.volatility,
            entry.volume,
            entry.market_condition,
            entry.outcome,
            entry.profit_loss,
            entry.notes,
            entry.created.isoformat(),
        )

        self.database.connection.execute(query, values)
        self.database.connection.commit()


    def all(self):
        query = """
        SELECT *
        FROM journal
        ORDER BY id DESC
        """

        cursor = self.database.connection.execute(query)

        return cursor.fetchall()


    def latest(self, limit=10):
        query = """
        SELECT *
        FROM journal
        ORDER BY id DESC
        LIMIT ?
        """

        cursor = self.database.connection.execute(query, (limit,))

        return cursor.fetchall()