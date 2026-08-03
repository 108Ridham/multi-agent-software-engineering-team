from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from services.repository_service import RepositoryService


class WriteFileToolInput(BaseModel):
    repository_url: str = Field(
        default="",
        description="GitHub repository URL (optional if repo is already cloned)."
    )

    file_path: str = Field(
        ...,
        description="Relative path of the file inside the repository (e.g. 'src/main.py')."
    )

    content: str = Field(
        ...,
        description="New content to write into the file."
    )


class WriteFileTool(BaseTool):
    """
    Tool for writing content to a file inside a cloned repository.
    """

    name: str = "WriteFileTool"

    description: str = (
        "Writes or overwrites the contents of a file inside a cloned repository. "
        "Pass the repository_url, the relative file_path inside the repo, and the new content."
    )

    args_schema: Type[BaseModel] = WriteFileToolInput

    repository_service: RepositoryService = Field(
        default_factory=RepositoryService
    )

    def _run(
        self,
        repository_url: str,
        file_path: str,
        content: str,
    ) -> str:

        try:
            repo_path = self.repository_service.get_repository_path(repository_url)
            full_path = repo_path / file_path

            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")

            return f"Successfully wrote '{file_path}'."

        except Exception as e:
            return f"Error writing file '{file_path}': {str(e)}"