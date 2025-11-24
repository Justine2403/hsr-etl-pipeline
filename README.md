# Honkai: Star Rail - Character Data Pipeline
This repository contains a data engineer project built around **Honkai: Star Rail** character information.
The objective is to design a complete workflow ETL that retrieves raw game data, organizes it into a structured format, and produces meaningful insights such as character summaries and build evaluations.

## Extraction
We use [EnkaNetwork API](https://github.com/EnkaNetwork/API-docs) to extract data from player profiles. Data is collected by sending requests to the API, which returns detailed information about:

- Players: general profile data such as UID, nickname, and level
- Characters: Characters informations displayed in the Character Showcase
- Builds: lightcone, relics and stats for each character from the Character Showcase

This approach allows automated, structured data collection for analysis without manual data entry.

## Transformation
