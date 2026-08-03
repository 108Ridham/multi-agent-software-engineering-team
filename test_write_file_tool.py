from tools.write_file_tool import WriteFileTool

tool = WriteFileTool()

print(
    tool.run(
        repository_path="repositories/requests",
        file_path="sample.txt",
        content="Hello from WriteFileTool!"
    )
)