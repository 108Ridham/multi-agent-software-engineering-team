from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from services.repository_service import RepositoryService


class CloneRepositoryToolInput(BaseModel):
    repository_url: str = Field(
        ...,
        description="GitHub repository URL to clone."
    )


class CloneRepositoryTool(BaseTool):
    """
    Tool for cloning a GitHub repository.
    """

    name: str = "CloneRepositoryTool"

    description: str = (
        "Clone a GitHub repository locally and return its local path."
    )

    args_schema: Type[BaseModel] = CloneRepositoryToolInput

    repository_service: RepositoryService = Field(
        default_factory=RepositoryService
    )

    def _run(self, repository_url: str) -> str:
        """
        Clone the repository and return the local path.
        """

        try:
            repository = self.repository_service.clone_repository(repository_url)
            return str(repository.local_path)

        except Exception as e:
            return f"Error cloning repository: {str(e)}"