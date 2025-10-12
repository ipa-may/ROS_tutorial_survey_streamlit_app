# ROS Tutorial Catalog

Streamlit interface for exploring tutorials listed in [`tutorial_list.yaml`](tutorial_list.yaml). Use the options below to run and develop the app with Docker Compose, VS Code Dev Containers, or a local Python environment.

![Catalog View](images/app_view_catalog.png)
![Charts View](images/app_view_charts.png)

## Run with Docker Compose

- Build and start the base image (runs `python3 streamlit_app.py` inside the container to validate dependencies; it exits once the script finishes):

  ```sh
  docker compose -f docker/docker-compose.yml up local-streamlit-built
  ```

- For the Streamlit dev server with live reload and a mounted workspace:

  ```sh
  docker compose -f docker/docker-compose.yml up local-streamlit-run
  ```

- Visit http://localhost:8501 when using the dev server (`local-streamlit-run` maps host 8501 ➜ container 8501). Stop that service with `Ctrl+C` before starting anything else on the same port.
- Stop services with:
  ```sh
  docker compose -f docker/docker-compose.yml down
  ```

## VS Code Dev Container

- Requires the Dev Containers extension (or GitHub Codespaces)
- Run “Dev Containers: Reopen in Container” from the command palette; the environment uses `mcr.microsoft.com/devcontainers/python:3.11`
- Post-create script installs helpful shell aliases (see `.devcontainer/bashrc.sh`)
- Base image ships with Python 3.11, `pip`, `pipx`, `pytest`, Git, and other common CLI utilities; add extra linters (e.g., Ruff, Flake8) via `pip install` as needed
- Launch the app with `streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501`

## Run Natively

- Create an isolated environment:
  ```
  python3 -m venv .venv && source .venv/bin/activate
  ```
- Upgrade build tooling: `pip install --upgrade pip`
- Install project deps: `pip install -r requirements.txt`
- Start the UI: `streamlit run streamlit_app.py`
- Visit http://localhost:8501 and exit with `Ctrl+C` when done

## Adding Tutorials

- Edit [`tutorial_list.yaml`](tutorial_list.yaml); each entry is a YAML mapping describing one tutorial
- Required fields: `name`, `organization`, and at least one of `doc-link` or `repo-link`
- Optional metadata (e.g., `language`, `ros_distro`, `robot-type`) improves filtering and analytics in the app
- Values that can take multiple items (like `ros_distro`, `robot-type`) may be written as YAML lists or comma-separated strings
- After saving, restart or refresh the Streamlit app to load the new entry
