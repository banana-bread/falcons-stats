# Ottawa Falcons FC Stats Tracker

## Overview

A Python-based web scraping and API project that:

- Automatically collects soccer statistics from OCSL website
- Stores data in a SQLite database
- Provides stats via API endpoints for [Ottawa Falcons](https://ottawafalcons.com/) soccer club teams

> **Note:** This project is currently under active development. Some features may change or be incomplete.

## Tech Stack

- Python
- Flask
- SQLite
- AWS EC2
- Nginx
- Poetry
- Terraform
- GitHub Actions

## Local Setup

### Initial Setup

1. Ensure `poetry` is installed. See [system requirements/installation guide](https://python-poetry.org/docs/#system-requirements)

2. Install dependencies

```bash
poetry install
```

3. Create local `/instance/config.py` based on `/instance/config.example.py`

4. Initialize database

```bash
poetry run init_db
```

5. Seed database with test data

```bash
poetry run seed_dev_db
```

6. Start development server

```bash
poetry run dev
```

### Debugging

Use [iPdb](https://pypi.org/project/ipdb/) for interactive debugging:

```python
import ipdb; ipdb.set_trace()
```

## Production Deployment

Automated via GitHub Actions:

- `terraform-plan.yml` runs on pull requests to main
- `terraform-apply.yml` runs on merges to main, updates infrastucture
- `deploy.yml` runs on merges to main, updates production code

### Initial Server Setup

1. Install dependencies

```bash
sudo dnf install git python3
python3 -m pip install --user pipx
pipx install poetry
```

2. Setup api and scheduler services with systemd

`falcons-stats-api.service`

```ini
[Unit]
Description=Gunicorn service for Falcons Stats Flask API
After=network.target

[Service]
User=ssm-user
WorkingDirectory=<working-dir>
ExecStart=poetry run gunicorn --workers 2 --bind 0.0.0.0:8080 'falcons_stats:create_app()'
Restart=always

[Install]
WantedBy=multi-user.target
```

`falcons-stats-scheduler.service`

```ini
[Unit]
Description=Falcons Stats Scheduler Service
After=network.target

[Service]
User=ssm-user
WorkingDirectory=/home/ssm-user/falcons-stats
ExecStart=/home/ssm-user/.local/bin/poetry run scheduler
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and Start Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable falcons-stats-api falcons-stats-scheduler
sudo systemctl start falcons-stats-api falcons-stats-scheduler
```

Check Service Status

```bash
sudo systemctl status falcons-stats-api
sudo systemctl status falcons-stats-scheduler
```

3. Nginx Reverse Proxy Configuration

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

Note: Most deployment tasks are now automated through GitHub Actions

## Logging

- Structured, machine-parsable JSON logging (mostly followed best practices from [this guide](https://betterstack.com/community/guides/logging/how-to-start-logging-with-python/#structured-json-logging-in-python))
- CloudWatch support in production

## API Endpoints

Access leading scorers via:

```
http://domain.com/leading-scorers
```

Access leading kepers via:

```
http://domain.com/leading-keepers
```

## Project Roadmap

### Current TODOs

- [ ] Replace mock data with actual data in scrapers (waiting on season to start for HTML tables to be present)
- [ ] Finish adding seeds for all Falcons teams/divs (waiting on all teams to register)
- [ ] Better error handling and logging (scrapers, api endpoints)

### Future Enhancements

- [ ] Add support for database migrations
- [ ] Scrape more data (schedules, team standings, etc)
- [ ] Capture stats from all divisions/teams
- [ ] Run scheduler service as more granular background jobs
- [ ] Enhance observability with performance metrics, execution tracking, and resource monitoring for scheduled tasks
