from tools.repository_scanner_tool import RepositoryScannerTool

tool = RepositoryScannerTool()

print(
    tool.run(
        repository_url="https://github.com/psf/requests.git"
    )
)