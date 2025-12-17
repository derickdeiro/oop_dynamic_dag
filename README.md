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

## How the project is configured and how DAGs are created dynamically

This codebase uses an object‑oriented design to standardize and reuse the ETL flow (Extract → Transform → Load) and to generate DAGs dynamically from simple, per‑source descriptions.

- DAG entry point: `dags/dynamic_dag.py` walks `projects/get_data_project/**` looking for `dag_info.py` files. For each `dag_info.py` found, it imports the module and reads the `main_dag` dictionary.
- OOP contracts (Core): `projects/core/elt_core.py` contains the abstract base classes `ExtractData`, `TransformData`, and `LoadData`. Each source implements concrete versions in its own `extract.py`, `transform.py`, and `load.py` files.
- Pipeline orchestration: `projects/core/pipeline.py` exposes the `PipelineConstructor` class, responsible for:
	- `set_dag_settings(...)`: building DAG configuration (id, description, `start_date`, `schedule`, `catchup`, `tags`, and `default_args` with owner, retries, and exponential backoff). Default timezone: `America/Sao_Paulo`.
	- `etl_tasks(...)`: defining the three tasks `Extract_Data`, `Transform_Data`, and `Load_Data` with `airflow.sdk.task`, chaining `extract >> transform >> load`, and passing `logical_date` into each step.

### How each dynamic DAG is created
1) Discovery: `dynamic_dag.py` uses `os.walk` + `importlib` to load each `dag_info.py` under `projects/get_data_project/<source>/`.
2) DAG description: each `dag_info.py` must expose a `main_dag` dictionary with metadata and the ETL classes. Minimal example:

```python
from projects.get_data_project.my_source.extract import ExtractDataMySource
from projects.get_data_project.my_source.transform import TransformDataMySource
from projects.get_data_project.my_source.load import LoadDataMySource

main_dag = {
		'dag_name': 'My_Source',
		'dag_description': 'ETL pipeline for My Source',
		'start_date': '2025-08-01',
		'schedule_interval': '@daily',
		'extract_class': ExtractDataMySource,
		'transform_class': TransformDataMySource,
		'load_class': LoadDataMySource,
		'tags': ['my_source', 'etl'],  # optional
}
```

3) DAG configuration: `PipelineConstructor.set_dag_settings(...)` converts fields (e.g., `start_date` into a `pendulum` datetime) and applies `default_args` (e.g., `owner='Data_Owner'`, `retries=3`, `retry_delay=1 min`, exponential backoff). `catchup` is `False` by default.
4) Task creation: `etl_tasks(...)` defines the ETL tasks with `@task` (`airflow.sdk.task`) and chains execution `extract -> transform -> load`.
5) Registration in Airflow: a `@dag(**dag_settings)` is created dynamically for each source, with `dag_id = dag_name`, `schedule = schedule_interval`, and `tags` as defined.

### How to add a new source
- Create the folder `projects/get_data_project/<source_name>/` containing:
	- `extract.py`: implements `ExtractData.extract_data(exec_date)` and returns raw data.
	- `transform.py`: implements `TransformData.transform_data(data, exec_date)` and returns transformed data.
	- `load.py`: implements `LoadData.load_data(data, exec_date)` to persist/publish data.
	- `dag_info.py`: defines `main_dag` with `dag_name`, `dag_description`, `start_date`, `schedule_interval`, optional `tags`, and the three classes.
- Save the files: the scheduler will detect the new DAG automatically; no changes are needed in `dags/`.

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
