# Readme 2048

Play the game of 2048 directly in your GitHub readme! This project provides a Flask server that manages 2048 game state, processes moves via HTTP requests, and automatically updates your GitHub profile readme (or any specified file) with the current game board.

## Customizing

When the server updates the readme file, it completely replaces the current file. If you host this, you will likely want to customize the non-game part of the readme. To do this, simply edit the markdown files in `./src/templates`:

- **game.md**: Renders the game board. You likely do not want to change this.
- **personal.md**: Contains all non-game information. Add your regular readme content here.
- **combined_readme.md**: Combines the previous two files. Change this only if you want to adjust their order or add another file.

All files use [Jinja templating](https://jinja.palletsprojects.com/en/stable/).

## Routes

- `/setup`: Use for initial setup.
- `/click/<int>`: Make a move in the game. The integer represents the move direction:
  - `1` = Up
  - `2` = Down
  - `3` = Left
  - `4` = Right

**Notes:**
- All routes redirect to the url specified in the `REDIRECT_URL` environment variable.

## Environment Variables

Set the following environment variables in your `.env` file:

- `PRODUCTION`: `'True'` or `'False'` to specify the environment.
- `DATABASE_URI`: Connection URI for your database (e.g., `postgresql://user:password@host:port/dbname`).
- `SECRET_KEY`: Secure random string for session security.
- `GIT_REPOS_DIR`: Directory where git repositories are cloned.
- `REDIRECT_URL`: URL to redirect to after an update.
- `REPO_CLONE_URL`: URL of the repository to clone and update.
- `UPDATE_FILE_PATH`: Path of the file to update, relative to the repository root.
- `WORKING_DIR`: Directory where the application will run.
- `GIT_NAME`: Git user name for commits.
- `GIT_EMAIL`: Git user email for commits.
- `SSH_DIR`: Directory containing SSH keys.

Refer to `.env.template` for example values.

## Running / Deployment

You can deploy this project using Docker or by running it directly. Docker is recommended for simplicity, but both methods are supported. Whichever you choose, it is recommended to put this behind a reverse proxy. Your SSH key must have write access to the repository to allow pushing.

### Docker

It is recommended you use the provided `compose.yaml` file in the root of the repository for recommended defaults. If used you should update the volumes to match you setup and change to postgres password.

**Volumes to Mount:**
- **SSH Keys**: Generate your SSH keys outside Docker and mount them into the container.
- **Repos Folder**: Mount an empty folder for repositories; the container will populate it. This allows persistence across restarts without needing to hit the `/setup` endpoint again.

**Example Docker Run Command:**
```bash
docker run \
  -v "/home/user/.ssh:/app/.ssh:ro" \
  -v "./repos:/app/repos:rw" \
  --env-file .env \
  -p 5000:5000 \
  ky42/readme-2048:latest
```

**Notes:**
- If you use a reverse proxy in the same Docker Compose setup, you do not need to expose ports on this container.
- Ensure your `.env` file is properly configured before starting the server.

### Running Directly

You can run the project directly on your machine without Docker. The following instructions use [Poetry](https://python-poetry.org), but you may use any Python environment manager.

**Steps:**

1. **Install dependencies:**
    ```bash
    poetry install
    ```

2. **(Optional) Add gunicorn for production:**
    ```bash
    poetry add gunicorn
    ```

3. **Start the server:**
    - For development:
        ```bash
        poetry run flask --app src run
        ```
    - For production (recommended):
        ```bash
        poetry run gunicorn --workers 1 src:app
        ```

**Notes:**
- Ensure your `.env` file is properly configured before starting the server.
- Only use one worker with gunicorn to avoid race conditions.

## License

This project is licensed under the MIT License.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.