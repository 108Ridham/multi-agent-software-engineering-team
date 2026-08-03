from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from services.scanner_service import RepositoryScannerService


class RepositoryScannerToolInput(BaseModel):
    repository_url: str = Field(
        ...,
        description="GitHub repository URL to scan."
    )


class RepositoryScannerTool(BaseTool):

    name: str = "RepositoryScannerTool"

    description: str = (
        "Analyze a cloned repository and detect its language, framework, "
        "package manager, entry point, Docker support, GitHub Actions, "
        "and other important metadata."
    )

    args_schema: Type[BaseModel] = RepositoryScannerToolInput

    scanner: RepositoryScannerService = Field(
        default_factory=RepositoryScannerService
    )

    def _run(self, repository_url: str) -> str:

        result = self.scanner.scan_repository(repository_url)

        return (
            f"Language: {result.language}\n"
            f"Framework: {result.framework}\n"
            f"Package Manager: {result.package_manager}\n"
            f"Entry Point: {result.entry_point}\n"
            f"README: {result.has_readme}\n"
            f"Docker: {result.has_docker}\n"
            f"GitHub Actions: {result.has_github_actions}"
        )