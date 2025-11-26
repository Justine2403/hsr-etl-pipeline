# Honkai: Star Rail - Character Data ETL Pipeline
This repository contains a data engineer project built around **Honkai: Star Rail** character information.
The objective is to design a complete workflow ETL that retrieves raw game data, organizes it into a structured format, and produces meaningful insights such as character summaries and build evaluations.

## Dependency management with Poetry

This project uses Poetry to manage the Python environment and dependencies. Poetry provides several benefits that make it ideal for ETL pipelines and Data Engineering projects:
- Isolated virtual environment (venv): automatically creates a dedicated Python environment for the project
  - Ensures no conflicts with other projects or global Python packages
  - Keeps your project easy to reproduce on another machine.

- Dependency and version management (pyproject.toml and poetry.lock)
  - `pyproject.toml` lists all project dependencies
  - `poetry.lock` locks exact versions, ensuring that everyone running the project uses the same versions of packages

- Separation of dev and prod dependencies: avoid installing unnecessary packages in production environments
  - Dev dependencies include tools for testing and formatting
  - Prod dependencies include libraries required to run the project

- Easy script execution (poetry run): guarantees that scripts always run in the correct environment with the right dependencies

## Extraction
We use [EnkaNetwork API](https://github.com/EnkaNetwork/API-docs) to extract data from player profiles. Data is collected by sending requests to the API, which returns detailed information about:

- Players: general profile data such as UID, nickname, and level
- Characters: Characters informations displayed in the Character Showcase
- Builds: lightcone, relics and stats for each character from the Character Showcase

This approach allows automated, structured data collection for analysis without manual data entry.

## Transformation
