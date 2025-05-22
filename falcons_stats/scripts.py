import subprocess
import os
from pathlib import Path

def run_dev_server():
    run_in_project_root(["flask", "--app", "falcons_stats", "run", "--debug", "--port", "8000"])

def run_init_db():
    run_in_project_root(["flask", "--app", "falcons_stats", "init-db"])

def run_seed_dev_db():
    run_in_project_root(["flask", "--app", "falcons_stats", "seed-dev-db"])

def run_seed_prod_db():
    run_in_project_root(["flask", "--app", "falcons_stats", "seed-prod-db"])

def run_scheduler():
    run_in_project_root(["flask", "--app", "falcons_stats", "run-scheduler"])

def run_scraper():
    """Run a specific scraper by name"""
    import sys
    if len(sys.argv) < 2:
        print("Error: Scraper name is required")
        print("Usage: poetry run scraper <scraper_name>")
        print("To see available scrapers, run: poetry run list-scrapers")
        return

    scraper_name = sys.argv[1]
    run_in_project_root(["flask", "--app", "falcons_stats", "run-scraper", scraper_name])

def list_scrapers():
    """List all available scrapers"""
    run_in_project_root(["flask", "--app", "falcons_stats", "list-scrapers"])

def find_project_root():
    """Find the project root by looking for pyproject.toml"""
    current_dir = Path.cwd()

    # Look in current directory and all parents
    while current_dir != current_dir.parent:
        if (current_dir / "pyproject.toml").exists():
            return str(current_dir)
        current_dir = current_dir.parent

    # If we can't find it, default to current directory
    return str(Path.cwd())

def run_in_project_root(command):
    """Run a command from the project root directory"""
    project_root = find_project_root()
    os.chdir(project_root)
    subprocess.run(command, check=True)
