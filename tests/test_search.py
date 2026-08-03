from services.search_service import CodeSearchService

url = "https://github.com/psf/requests.git"

service = CodeSearchService()

results = service.search(
    url,
    "Session"
)

for file in results:
    print(file)