from services.scanner_service import RepositoryScannerService

scanner = RepositoryScannerService()

result = scanner.scan_repository(
    "https://github.com/psf/requests.git"
)

print(result)