# oop_dynamic_dag
Repository demonstrating dynamic DAGs using OOP
# OOP Dynamic DAG (Airflow + Astro)

This repository contains an Airflow project structured to generate dynamic DAGs using an object‑oriented approach. It is designed to run locally using the Astronomer CLI (Astro), simplifying the Airflow developer workflow on Linux.

## Prerequisites
- Git installed
- Linux (tested on Ubuntu/Debian‑based distros)
- Docker Engine and Docker Compose installed and running
- Astronomer CLI (Astro) installed

If you don’t have Docker, follow the official docs for your distro: https://docs.docker.com/engine/install/

## Clone the Repository
```bash
git clone https://github.com/derickdeiro/oop_dynamic_dag
cd oop_dynamic_dag
```

## Install Astronomer CLI (Astro) on Linux
Astronomer provides an install script for Linux. Run:
```bash
curl -sSL https://install.astronomer.io | sudo bash
```

### For other operating systems, see:

https://www.astronomer.io/docs/astro/cli/install-cli

Verify installation:
```bash
astro version
```

If the command is not found, ensure `~/.astro/bin` is on your PATH or reopen the terminal.

## Project Structure (overview)
- `dags/` contains the dynamic DAG entry point
- `projects/` holds core pipeline logic and per‑source steps (`extract.py`, `transform.py`, `load.py`, `dag_info.py`)
- `Dockerfile`, `requirements.txt`, and `pyproject.toml` define the environment
- `airflow_settings.yaml` can preload connections/variables

## Start the Airflow project (Astro dev)
From the repository root:
```bash
astro dev start
```

This will:
- Build the Airflow image and start `webserver`, `scheduler`, and `postgres`
- Mount local code into the containers for rapid iteration

Once started, open the Airflow UI:
- Default: http://localhost:8080
- Default credentials: `airflow` / `airflow` (unless customized)

## Stop the environment
```bash
astro dev stop
```

## Common Development Commands
- Rebuild after dependency changes:
```bash
astro dev restart
```
- See container logs:
```bash
astro dev logs
```
- Run tests (if configured):
```bash
astro dev run pytest
```

## Troubleshooting
- Docker not running: start Docker service (`sudo systemctl start docker`) and re‑run `astro dev start`.
- Port 8080 in use: stop other services using that port or change the port in `.astro/config.yaml` if present.
- Dependency changes not reflected: run `astro dev restart` to rebuild containers.
- Permissions on install script: use `sudo` for the Astro installer, or ensure your user can write to `/usr/local/bin`.

## Notes
- Make sure your user can run Docker without `sudo` (optional). If not, you may need to prefix Docker commands with `sudo`, or add your user to the `docker` group.
- If you customize Airflow connections or variables, place them in `airflow_settings.yaml` and restart the environment.

## Next Steps
- Explore `projects/core/pipeline.py` and `projects/get_data_project/**` to understand the OOP layout.
- Add new sources by creating a new folder under `projects/get_data_project/<source_name>/` with `dag_info.py`, `extract.py`, `transform.py`, and `load.py`.
