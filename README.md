# Ottawa Falcons FC Stats Tracker

## Overview

A Python-based web scraping and API project that:

- Automatically collects soccer statistics from OCSL website
- Stores data in a SQLite database
- Provides RESTful API endpoints for Ottawa Falcons team stats

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

1. Install dependencies

```bash
$ poetry install
```

2. Create local `/instance/config.py` based on `/instance/config.example.py`

3. Initialize database

```bash
$ poetry run flask --app falcons_stats init-db
```

4. Seed database with test data

```bash
$ poetry run flask --app falcons_stats seed-dev-db
```

5. Start development server

```bash
$ poetry run dev
```

### Debugging

Use iPdb for interactive debugging:

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

2. Nginx Reverse Proxy Configuration

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

- Structured JSON logging (mostly followed best practices from [this guide](https://betterstack.com/community/guides/logging/how-to-start-logging-with-python/#structured-json-logging-in-python))
- CloudWatch support in production

## API Endpoints

Access leading scorers via:

```
http://domain.com/leading-scorers
```

Access leading kepers via:

```
http://domain.com/keepers-scorers
```
