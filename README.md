## Falcons Stats Project

A Python-based project for scraping, managing, and serving soccer stats for Ottawa Falcons FC. This project includes a SQLite database, API, and scraping scripts for populating and updating the database.

## Prerequisites

- python (required version defined in `pyproject.toml`)
- poetry
- sqlite3

## Setup

### 1. Install dependencies with poetry

```
$ poetry install
```

### 2. Create the sqlite database

```
$ sqlite3 falcons-stats.db
```

### 3. Create the database schema

```
$ poetry run python scripts/create_db.py
```

### 4. Seed the database

```
$ poetry run python scripts/seed_data.py
```

### 5. To run flask server

```
$ flask --app falcons_stats.api run
```

## Deploy to production

- Infra described in `main.tf` see the `terraform-plan` is run when pr's are opened against main, `terraform-apply` is run on merges to main

### Using aws session manager

prerequisites:

- session-manager-plugin
- aws-cli

1. Find instance id (should make this a script really)

```
aws ec2 describe-instances --filters "Name=tag:Name,Values=FalconsStatsEC2Instance" --query "Reservations[].Instances[].InstanceId" --output text
```

2. connect to target

```
aws ssm start-session --target <instance_id>
```
