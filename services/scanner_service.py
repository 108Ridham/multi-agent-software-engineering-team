from pathlib import Path

from models.repository_scan_models import RepositoryScanResult
from services.repository_service import RepositoryService


class RepositoryScannerService:

    def __init__(self):
        self.repository_service = RepositoryService()

    def scan_repository(self, repo_url: str):

        repo_path = self.repository_service.get_repository_path(repo_url)

        files = {p.name.lower(): p for p in repo_path.rglob("*") if p.is_file()}

        language = "Unknown"
        framework = "Unknown"
        package_manager = "Unknown"
        entry_point = "Unknown"

        # ---------- Python ----------
        if "requirements.txt" in files or "pyproject.toml" in files:
            language = "Python"

            if "pyproject.toml" in files:
                package_manager = "Poetry / UV"

                content = files["pyproject.toml"].read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()

                if "fastapi" in content:
                    framework = "FastAPI"

                elif "django" in content:
                    framework = "Django"

                elif "flask" in content:
                    framework = "Flask"

            if "requirements.txt" in files:
                package_manager = "pip"

                content = files["requirements.txt"].read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()

                if "fastapi" in content:
                    framework = "FastAPI"

                elif "django" in content:
                    framework = "Django"

                elif "flask" in content:
                    framework = "Flask"

        # ---------- Node ----------
        elif "package.json" in files:
            language = "JavaScript / TypeScript"
            package_manager = "npm"

        # ---------- README ----------
        has_readme = any(
            name.startswith("readme")
            for name in files
        )

        # ---------- Docker ----------
        has_docker = "dockerfile" in files

        # ---------- GitHub Actions ----------
        has_github_actions = (
            repo_path / ".github" / "workflows"
        ).exists()

        # ---------- Entry Point ----------
        for candidate in [
            "main.py",
            "app.py",
            "manage.py",
            "server.py",
        ]:

            if candidate in files:
                entry_point = candidate
                break

        return RepositoryScanResult(
            language=language,
            framework=framework,
            package_manager=package_manager,
            has_readme=has_readme,
            has_docker=has_docker,
            has_github_actions=has_github_actions,
            entry_point=entry_point,
        )