from tools.code_search_tool import CodeSearchTool

tool = CodeSearchTool()

result = tool.run(
    repository_url="https://github.com/psf/requests.git",
    query="Session"
)

print(result)