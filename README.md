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

### 3. Initialize sqlite database

```
$ poetry run flask --app falcons_stats init-db
```

### 4. Seed the database

```
$ poetry run python scripts/seed_data.py
```

### 5. To run flask dev server

```
$ poetry run flask --app falcons_stats run --debug
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

### Setting up production server

1. install git

```
sudo dnf install git
```

2. install python3

```
sudo dnf install python3
```

3. install pipx

```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
source ~/.bashrc
```

4. install poetry with pipx

```
pipx install poetry
```

5. this is a no-no for prod, but I tested this with the dev server, and accessed the api from the servers public dns

```
poetry run flask --app test_api.app run -h 0.0.0.0 -p 8080
```

6. then, visit

```
ec2-18-235-149-176.compute-1.amazonaws.com:8080/leading-scorers
```

### Running Flask API with systemd:

[Running a Flask Application as a service with Systemd](https://blog.miguelgrinberg.com/post/running-a-flask-application-as-a-service-with-systemd)

Example configuration file:

```
[Unit]
Description=<a description of your application>
After=network.target

[Service]
User=<username>
WorkingDirectory=<path to your app>
ExecStart=<app start command>
Restart=always

[Install]
WantedBy=multi-user.target
```

Unit configuration files are added in the /etc/systemd/system directory to be seen by systemd. Each time you add or modify a unit file you must tell systemd to refresh its configuration:

```
$ sudo systemctl daemon-reload
```

And then you can use the systemctl <action> <service-name> command to start, stop, restart or obtain status for your service:

```
sudo systemctl start falcons-stats
sudo systemctl stop falcons-stats
sudo systemctl restart falcons-stats
sudo systemctl status falcons-stats
```

### Setup reverse proxy with nginx to route traffic from port 80 to 8080

Cannot run Gunicorn server on port 80 without root privileges, so a way around that is to run in on 8080, and use nginx as a reverse proxy to route traffic from 80 -> 8080.

1. Install nginx

```
sudo dnf install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

2. Add this config file at /etc/nginx/conf.d/falcons-stats.conf

```
server {
    listen 80;
    server_name ec2-18-235-149-176.compute-1.amazonaws.com;

    location / {
        proxy_pass http://127.0.0.1:8080;  # Gunicorn/Falcon is running on port 8080
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

3. test the config to avoid any errors

```
sudo nginx -t
```

4. restart nginx to apply changes

```
sudo systemctl restart nginx
```

5. bonus: make sure nginx starts automatically when the server restarts:

```
sudo systemctl enable nginx
```
