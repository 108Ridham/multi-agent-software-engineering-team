from services.file_service import FileService

# Replace with your cloned repository path
REPO_PATH = "repositories/requests"

service = FileService(REPO_PATH)

print("=" * 50)
print("Testing FileService")
print("=" * 50)

# -----------------------------
# Test 1: Check repository exists
# -----------------------------
print("\nTest 1: Repository Exists")

print(service.exists("README.md"))


# -----------------------------
# Test 2: Read File
# -----------------------------
print("\nTest 2: Read File")

content = service.read_file("README.md")

print(content[:300])


# -----------------------------
# Test 3: Write File
# -----------------------------
print("\nTest 3: Write File")

service.write_file(
    "test_output.txt",
    "Hello from FileService!"
)

print("File written successfully.")


# -----------------------------
# Test 4: Read Written File
# -----------------------------
print("\nTest 4: Read Written File")

print(service.read_file("test_output.txt"))


# -----------------------------
# Test 5: Append File
# -----------------------------
print("\nTest 5: Append File")

service.append_file(
    "test_output.txt",
    "\nThis line was appended."
)

print(service.read_file("test_output.txt"))


# -----------------------------
# Test 6: Exists
# -----------------------------
print("\nTest 6: Exists")

print(service.exists("test_output.txt"))


# -----------------------------
# Test 7: Create Directory
# -----------------------------
print("\nTest 7: Create Directory")

service.create_directory("test_folder")

print(service.exists("test_folder"))

print("\nAll tests completed successfully.")