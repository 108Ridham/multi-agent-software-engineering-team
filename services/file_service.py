from pathlib import Path


class FileService:
    """
    Handles all file operations inside the cloned repository.
    Prevents access outside the repository root.
    """

    def __init__(self, repository_root: str):
        self.repository_root = Path(repository_root).resolve()


    def _resolve_path(self, relative_path: str) -> Path:
        """
        Resolve a relative path safely inside the repository.
        """

        file_path = (self.repository_root / relative_path).resolve()

        try:
            file_path.relative_to(self.repository_root)
        except ValueError:
            raise ValueError("Access outside repository is not allowed.")

        return file_path


    def read_file(self, relative_path: str) -> str:
        """
        Read and return the contents of a file.
        """

        file_path = self._resolve_path(relative_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        if not file_path.is_file():
            raise IsADirectoryError(f"{relative_path} is not a file.")

        return file_path.read_text(encoding="utf-8")


    def write_file(self, relative_path: str, content: str) -> None:
        """
        Create or overwrite a file.
        """

        file_path = self._resolve_path(relative_path)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")


    def append_file(self, relative_path: str, content: str) -> None:
        """
        Append content to an existing file.
        Creates the file if it does not exist.
        """

        file_path = self._resolve_path(relative_path)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content)


    def exists(self, relative_path: str) -> bool:
        """
        Check whether a file or directory exists.
        """

        file_path = self._resolve_path(relative_path)
        return file_path.exists()


    def create_directory(self, relative_path: str) -> None:
        """
        Create a directory if it does not already exist.
        """

        directory = self._resolve_path(relative_path)
        directory.mkdir(parents=True, exist_ok=True)


    def delete_file(self, relative_path: str) -> None:
        """
        Delete a file.
        """

        file_path = self._resolve_path(relative_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        if not file_path.is_file():
            raise IsADirectoryError(f"{relative_path} is not a file.")

        file_path.unlink()