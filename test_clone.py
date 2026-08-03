from services.repository_service import RepositoryService

service = RepositoryService()

repo = service.clone_repository(
    "https://github.com/psf/requests.git"
)

print(repo)
print(repo.local_path)