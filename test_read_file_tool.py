from tools.read_file_tool import ReadFileTool


tool = ReadFileTool()

result = tool.run(
    repository_path="repositories/requests",
    file_path="README.md"
)

print("=" * 80)
print(result[:1000])
print("=" * 80)