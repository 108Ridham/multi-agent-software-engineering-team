from dataclasses import dataclass


@dataclass
class RepositoryScanResult:
    language: str
    framework: str
    package_manager: str
    has_readme: bool
    has_docker: bool
    has_github_actions: bool
    entry_point: str