from pathlib import Path
from typing import List

from services.repository_service import RepositoryService


class CodeSearchService:

    def __init__(self):
        self.repository_service = RepositoryService()

    def search(
        self,
        repo_url: str,
        query: str,
        case_sensitive: bool = False,
    ) -> List[Path]:

        files = self.repository_service.list_files(repo_url)

        matches = []

        for file in files:

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if not case_sensitive:
                    found = query.lower() in text.lower()
                else:
                    found = query in text

                if found:
                    matches.append(file)

            except Exception:
                continue

        return matches