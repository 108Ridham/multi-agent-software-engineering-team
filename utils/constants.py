from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPOSITORIES_DIR = PROJECT_ROOT / "repositories"

REPOSITORIES_DIR.mkdir(exist_ok=True)