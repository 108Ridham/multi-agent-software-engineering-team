from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from services.search_service import CodeSearchService


class CodeSearchToolInput(BaseModel):
    repository_url: str = Field(
        default="",
        description="GitHub repository URL or local path (optional if repo is already cloned)."
    )
    query: str = Field(
        ...,
        description="The keyword or text to search for."
    )


class CodeSearchTool(BaseTool):
    """Tool for searching keywords inside a cloned repository."""

    name: str = "CodeSearchTool"

    description: str = (
        "Search for classes, functions, variables, keywords, or any text "
        "inside a repository. Returns the matching file paths."
    )

    args_schema: Type[BaseModel] = CodeSearchToolInput

    search_service: CodeSearchService = Field(
        default_factory=CodeSearchService
    )

    def _run(self, repository_url: str, query: str) -> str:
        matches = self.search_service.search(
            repo_url=repository_url,
            query=query,
        )

        if not matches:
            return f"No files found containing '{query}'."

        return "\n".join(str(file) for file in matches)