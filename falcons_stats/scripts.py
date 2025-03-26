import subprocess

def run_dev_server():
    subprocess.run(["flask", "--app", "falcons_stats", "run", "--debug"], check=True)

def run_init_db():
    subprocess.run(["flask", "--app", "falcons_stats", "init-db"], check=True)

def run_seed_dev_db():
    subprocess.run(["flask", "--app", "falcons_stats", "seed-dev-db"], check=True)

def run_scheduler():
    subprocess.run(["flask", "--app", "falcons_stats", "run-scheduler"], check=True)
