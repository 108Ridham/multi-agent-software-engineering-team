from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

from services.repository_service import RepositoryService


class ReadFileToolInput(BaseModel):
    repository_url: str = Field(
        default="",
        description="GitHub repository URL (optional if repo is already cloned)."
    )

    file_path: str = Field(
        ...,
        description="Relative path of the file inside the repository (e.g. 'src/main.py')."
    )


class ReadFileTool(BaseTool):
    """
    Tool for reading the contents of a file from a cloned repository.
    """

    name: str = "ReadFileTool"

    description: str = (
        "Reads the contents of a file from a cloned repository and returns it as text. "
        "Pass the repository_url and the relative file_path inside the repo."
    )

    args_schema: Type[BaseModel] = ReadFileToolInput

    repository_service: RepositoryService = Field(
        default_factory=RepositoryService
    )

    def _run(
        self,
        repository_url: str,
        file_path: str,
    ) -> str:
        """
        Read and return the contents of a repository file.
        """

        try:
            repo_path = self.repository_service.get_repository_path(repository_url)
            full_path = repo_path / file_path

            if not full_path.exists():
                return f"File not found: {file_path}"

            return full_path.read_text(encoding="utf-8", errors="ignore")

        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"