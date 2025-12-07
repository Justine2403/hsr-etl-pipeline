# Honkai: Star Rail - Character Data ETL Pipeline
This repository contains a data engineer project built around **Honkai: Star Rail** character information.
The objective is to design a complete workflow ETL that retrieves raw game data, organizes it into a structured format, and produces meaningful insights such as character summaries and build evaluations.

## Dependency management with Poetry

This project uses **Poetry** to manage the Python environment and dependencies. Poetry provides several benefits that make it ideal for ETL pipelines and Data Engineering projects:
- Isolated virtual environment (venv): automatically creates a dedicated Python environment for the project
  - Ensures no conflicts with other projects or global Python packages
  - Keeps project easy to reproduce on another machine
- Dependency and version management
  - `pyproject.toml` lists all project dependencies
  - `poetry.lock` locks exact versions, ensuring that everyone running the project uses the same versions of packages
- Separation of dev and prod dependencies: avoid installing unnecessary packages in production environments
  - Dev dependencies include tools for testing and formatting
  - Prod dependencies include libraries required to run the project
- Script execution with `poetry run`: guarantees that scripts always run in the correct environment with the right dependencies

## Python version management with pyenv

Allow to switch between python version to make the differents librairies and techs work in the project.

## Extraction
We use [EnkaNetwork API](https://github.com/EnkaNetwork/API-docs) to extract data from player profiles. Data is collected by sending requests to the API using async/await, which returns detailed information about:

- Players: general profile data such as UID, nickname, and level
- Characters: Characters informations displayed in the Character Showcase
- Builds: lightcone, relics and stats for each character from the Character Showcase

This approach allows automated, structured data collection for analysis without manual data entry.

### Data Model
Player:
| Field      | Type   | Description          |
| ---------- | ------ | -------------------- |
| `uid`      | int    | Player account ID    |
| `nickname` | string | In-game player name  |
| `level`    | int    | Trailblaze level     |

Characters:
| Field              | Type   | Description                       |
| ------------------ | ------ | --------------------------------- |
| `character_id`     | int    | Unique character ID               |
| `name`             | string | Character name                    |
| `level`            | int    | Character level                   |
| `element`          | string | Character element                 |
| `light_cone`       | string | Equipped Light Cone               |
| `light_cone_level` | int    | Light Cone level                  |
| `player_uid`       | int    | Link to the Player (foreign key)  |

Stats:
| Field          | Type  | Description              |
| -------------- | ----- | ------------------------ |
| `character_id` | int   | Link to Character        |
| `HP`           | float | Total HP                 |
| `ATK`          | float | Total Attack             |
| `DEF`          | float | Total Defense            |
| `SPD`          | float | Speed                    |
| `CRIT Rate`    | float | Critical rate (0–1)      |
| `CRIT DMG`     | float | Critical damage (0–n)    |

Relics:
| Field                  | Type                     | Description                              |
| ---------------------- | ------------------------ | ---------------------------------------- |
| `relic_id`             | int                      | Unique relic identifier                  |
| `character_id`         | int                      | Character this relic belongs to          |
| `slot`                 | string                   | HEAD / HAND / BODY / FOOT / ROPE / ORBIT |
| `set_name`             | string                   | Relic set name                           |
| `rarity`               | int                      | Relic rarity                             |
| `main_stat_name`       | string                   | Main stat type                           |
| `main_stat_value`      | float                    | Main stat value                          |
| `main_stat_is_percent` | bool                     | Whether main stat is a percentage        |
| `substats`             | array of objects (max 4) | List of substats                         |

Relics stats:
| Field        | Type   | Description        |
| ------------ | ------ | ------------------ |
| `name`       | string | Substat type       |
| `value`      | float  | Substat value      |
| `is_percent` | bool   | Whether value is % |

## Application

Building an app with Streamlit where it shows users characters informations and its build 

## Deployement 

We will be using Airflow for the deployement of each scripts


