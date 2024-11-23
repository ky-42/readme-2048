"""Module for managing game rounds."""

from datetime import datetime
from typing import Optional, Tuple

import psycopg

from env import DATABASE_URI

# Create table if it doesn't exist
with psycopg.connect(DATABASE_URI()) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS round (
                id SERIAL PRIMARY KEY,
                score INT NOT NULL DEFAULT 0,
                biggest_block INT,
                end_date TIMESTAMPTZ,
                active BOOLEAN NOT NULL DEFAULT TRUE
            )
            """
        )


def start() -> None:
    """Starts a new round.

    Raises:
        Exception: If there is already an active round
    """

    with psycopg.connect(DATABASE_URI()) as conn:
        with conn.cursor() as cur:

            cur.execute("SELECT * FROM round WHERE active = TRUE")

            if cur.fetchone() is not None:
                raise Exception("Round already active")

            cur.execute("INSERT INTO round DEFAULT VALUES")


def add_score(score: int) -> None:
    """Adds to the score of the current round.

    Args:
        score (int): Score to add.

    Raises:
        Exception: If there is no active round.
    """

    with psycopg.connect(DATABASE_URI()) as conn:
        with conn.cursor() as cur:

            cur.execute("SELECT score FROM round WHERE active = TRUE")

            if (current_score_row := cur.fetchone()) is None:
                raise Exception("No active round")

            cur.execute(
                "UPDATE round SET score = %s WHERE active = TRUE",
                (current_score_row[0] + score,),
            )


def end(biggest_block: int, end_date: datetime) -> None:
    """Ends the current round.

    Args:
        biggest_block (int): The biggest block in the round.
        end_date (datetime): Date the round ended.

    Raises:
        Exception: If no active round
    """

    with psycopg.connect(DATABASE_URI()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM round WHERE active = TRUE")

            if cur.fetchone() is None:
                raise Exception("No active round")

            cur.execute(
                "UPDATE round SET (biggest_block, end_date, active) = (%s, %s, FALSE), WHERE active = TRUE",
                (biggest_block, end_date),
            )


def get_current_score() -> Optional[int]:
    """Gets the score of the current round.

    Returns:
        Optional, int: Score of the current round. None if no active round.
    """

    with psycopg.connect(DATABASE_URI()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT score FROM round WHERE active = TRUE")

        current_score = cur.fetchone()

        if current_score is None:
            return None

        return current_score[0]


def get_high_score() -> Optional[Tuple[int, datetime]]:
    """Gets the highest score recorded.

    Returns:
        Optional, Tuple[int, datetime]: Round with highest score. In form: [score, end date].
            None if no rounds have been played.
    """

    with psycopg.connect(DATABASE_URI()) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT score, end_date FROM round WHERE active = FALSE ORDER BY score DESC, end_date ASC LIMIT 1"
        )

        highest_score_record = cur.fetchone()

        if highest_score_record is None:
            return None

        return highest_score_record
