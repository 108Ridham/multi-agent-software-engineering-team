from pathlib import Path
from git import Repo
import shutil

from models.repository_models import RepositoryInfo
from utils.constants import REPOSITORIES_DIR


class RepositoryService:

    def __init__(self):
        self.base_path = REPOSITORIES_DIR

    def get_repository_name(self, repo_url: str) -> str:
        # Include owner segment to avoid collisions between repos with the same name
        # e.g. "octocat/Hello-World" → "octocat_Hello-World"
        parts = repo_url.rstrip("/").replace(".git", "").split("/")
        return "_".join(parts[-2:]) if len(parts) >= 2 else parts[-1]

    def get_repository_path(self, repo_url: str) -> Path:
        if repo_url:
            repo_name = self.get_repository_name(repo_url)
            exact_path = self.base_path / repo_name
            if exact_path.exists():
                return exact_path

        # Fallback: if exact path doesn't exist (e.g. placeholder URL or empty URL passed by LLM),
        # return the active cloned directory inside REPOSITORIES_DIR
        if self.base_path.exists():
            cloned_dirs = [d for d in self.base_path.iterdir() if d.is_dir() and not d.name.startswith(".")]
            if cloned_dirs:
                cloned_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
                return cloned_dirs[0]

        return self.base_path / (self.get_repository_name(repo_url) if repo_url else "repo")

    def repository_exists(self, repo_url: str) -> bool:
        return self.get_repository_path(repo_url).exists()

    def clone_repository(self, repo_url: str) -> RepositoryInfo:
        repo_path = self.get_repository_path(repo_url)

        if not repo_path.exists():
            Repo.clone_from(repo_url, repo_path)

        return RepositoryInfo(
            name=self.get_repository_name(repo_url),
            url=repo_url,
            local_path=repo_path,
        )

    def delete_repository(self, repo_url: str):
        repo_path = self.get_repository_path(repo_url)

        if repo_path.exists():
            shutil.rmtree(repo_path)

    # ---------- ADD THESE METHODS BELOW ----------

    def list_files(self, repo_url: str):
        repo_path = self.get_repository_path(repo_url)

        return [
            file
            for file in repo_path.rglob("*")
            if file.is_file()
        ]

    def read_file(self, repo_url: str, relative_path: str):
        repo_path = self.get_repository_path(repo_url)

        file_path = repo_path / relative_path

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_directory_tree(self, repo_url: str):
        repo_path = self.get_repository_path(repo_url)

        return [
            path.relative_to(repo_path)
            for path in repo_path.rglob("*")
        ]