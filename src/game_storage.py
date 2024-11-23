"""Module for storing and loading the current game state from storage."""

from typing import List, Optional, Tuple

import psycopg

from env import DATABASE_URI
from game import Game

with psycopg.connect(DATABASE_URI()) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS square (
                x INT,
                y INT,
                value INT DEFAULT 0 NOT NULL CHECK (value >= 0 AND value % 2 = 0),
                PRIMARY KEY (x, y)
            );
            """
        )


def load_or_new() -> Tuple[Game, bool]:
    """Attempts to load the current game from storage. If no game is found, a new game is started.

    Returns:
        Tuple[Game, bool]: The new or loaded game and bool stating if game was loaded.
            True if game was loaded, False if new game was started.
    """

    with psycopg.connect(DATABASE_URI()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM square")
            rows = cur.fetchall()

            dimensions = Game.get_dimensions()

            # Check if game data is valid
            start_new_game = False
            for row in rows:
                x, y, _ = row
                if x >= dimensions[1] or y >= dimensions[0]:
                    start_new_game = True
                    break

            if len(rows) != dimensions[0] * dimensions[1]:
                start_new_game = True

            # Start new game
            if start_new_game:
                new_game = Game()
                new_grid = new_game.get_grid()

                for y in range(dimensions[0]):
                    for x in range(dimensions[1]):
                        cur.execute(
                            "INSERT INTO square (x, y, value) VALUES (%s, %s, %s)",
                            (x, y, new_grid[y][x]),
                        )

                return new_game, False

            # Load old game
            else:
                game_grid = [
                    [0 for _ in range(dimensions[1])] for _ in range(dimensions[0])
                ]

                for row in rows:
                    x, y, value = row
                    game_grid[y][x] = value

                game = Game(game_grid)

                return game, True


def save(grid: List[List[int]], old_grid: Optional[List[List[int]]] = None) -> None:
    """Saves the current game to storage.

    Args:
        grid (List[List[int]]): The grid of the current game.
        old_grid (List[List[int]], optional): The grid of the current
            game when it was first loaded before any moves were made.
            Defaults to None.
    """

    dimensions = Game.get_dimensions()

    with psycopg.connect(DATABASE_URI()) as conn:
        with conn.cursor() as cur:
            for y in range(dimensions[0]):
                for x in range(dimensions[1]):
                    if old_grid is not None and grid[y][x] != old_grid[y][x]:
                        cur.execute(
                            "UPDATE square SET value = %s WHERE x = %s AND y = %s",
                            (grid[y][x], x, y),
                        )


def delete() -> None:
    """Removes the current game from storage."""

    with psycopg.connect(DATABASE_URI()) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE square")
