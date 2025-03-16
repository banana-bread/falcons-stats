import subprocess

def run_dev_server():
    subprocess.run(["flask", "--app", "falcons_stats", "run", "--debug"], check=True)