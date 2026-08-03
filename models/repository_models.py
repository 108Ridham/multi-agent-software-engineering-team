from dataclasses import dataclass
from pathlib import Path


@dataclass
class RepositoryInfo:
    name: str
    url: str
    local_path: Path