"""Module for running git commands."""

import subprocess
from pathlib import Path

from env import UPDATE_FILE_NAME, UPDATE_FILE_PATH


def update(update_string: str) -> None:
    """Update a file then push it to a git repository.

    Args:
        update_string (str): The string to write to the file.
    """

    update_path = Path(UPDATE_FILE_PATH())
    update_file_name = UPDATE_FILE_NAME()
    readme_file_path = update_path / update_file_name

    with open(readme_file_path, "w") as f:
        f.write(update_string)

    subprocess.run(["git", "add", update_file_name], cwd=update_path)
    subprocess.run(["git", "commit", "-m", "Update README"], cwd=update_path)
    subprocess.run(["git", "push", "-f"], cwd=update_path)
