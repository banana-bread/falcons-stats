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

### Misc

allow inbound traffic on port 22 (ssh) from my ip

```
aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port 22 \
  --cidr $(curl -s https://checkip.amazonaws.com)/32
```

revoke inbound traffic on port 22

```
aws ec2 revoke-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port 22 \
  --cidr $(curl -s https://checkip.amazonaws.com)/32
```

create ssh-key pair locally

```
ssh-keygen -t rsa -b 4096 -C "ssh-key-name" -f ssh-key-name

```

then associate it with the ec2 instance in `main.tf`

```
resource "aws_instance" "falcons_stats_server" {
  ami                    = "ami-053a45fff0a704a47"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instances.id]
  key_name               = "falcons-stats-server-ssh-key"
  tags = {
    Name = "FalconsStatsEC2Instance"
  }
}
```
