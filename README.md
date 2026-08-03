# Multi-Agent Software Engineering Team with CrewAI

An AI-powered multi-agent software engineering system built using **CrewAI**, **CrewAI Flows**, and **Ollama**.

The system can analyze an existing GitHub repository, understand its architecture, plan requested changes, conditionally select the required engineering agents, modify repository files, review the implementation, test it, and generate documentation.

The project is designed to run with **local LLMs through Ollama**, reducing dependency on paid cloud APIs.

---

## Overview

Traditional AI coding workflows often use a single model for repository analysis, planning, implementation, and review.

This project separates those responsibilities across specialized AI agents.

The workflow follows:

```text
GitHub Repository + User Request
              │
              ▼
    Repository Research Analyst
              │
              ▼
       Software Architect
              │
              ▼
      Conditional Routing
        /      |       \
       /       |        \
 Backend    Frontend    Database
 Engineer   Engineer    Engineer
       \       |        /
        \      |       /
              ▼
      Senior Code Reviewer
              │
              ▼
       QA & Test Engineer
              │
              ▼
 Technical Documentation
        Specialist
```

The conditional flow prevents unnecessary implementation agents from running when they are not required.

For example, a backend-only change does not need to invoke the Frontend or Database Engineer unless the requested implementation actually requires them.

---

## AI Agents

The system contains eight specialized agents.

### 1. Repository Research Analyst

Responsible for understanding an unfamiliar repository.

It can:

- Clone GitHub repositories
- Scan repository metadata
- Identify languages and frameworks
- Detect package managers
- Inspect repository structure
- Search source code
- Read important files
- Produce a repository analysis report

### 2. Software Architect

Uses the repository analysis and implementation request to determine how the requested feature should be implemented.

Responsibilities include:

- Architecture analysis
- Component identification
- Dependency analysis
- Implementation planning
- Technical risk identification
- Determining which implementation areas are required

### 3. Backend Software Engineer

Handles backend-related changes such as:

- APIs
- Endpoints
- Server-side logic
- Authentication/authorization logic
- Backend integrations
- Business logic

### 4. Frontend Software Engineer

Handles frontend-related changes such as:

- UI components
- Pages
- Forms
- Client-side functionality
- Frontend integrations

### 5. Database Engineer

Handles database-related changes such as:

- Schemas
- Tables
- Database models
- Queries
- Migrations
- Persistence logic

### 6. Senior Code Reviewer

Reviews implementation produced by the engineering agents.

It checks areas such as:

- Code quality
- Maintainability
- Potential bugs
- Security concerns
- Integration issues
- Engineering practices

### 7. QA & Test Engineer

Validates the implementation and identifies potential failures and edge cases.

### 8. Technical Documentation Specialist

Produces technical documentation describing the implementation and relevant project changes.

---

## Conditional Multi-Agent Pipeline

The project uses **CrewAI Flows** to control agent execution.

Instead of always executing:

```text
Research
→ Architect
→ Backend
→ Frontend
→ Database
→ Review
→ Testing
→ Documentation
```

the system can determine which implementation agents are actually necessary.

For example:

```text
Request:
"Add a new REST API health endpoint."
```

The workflow can route the request through:

```text
Repository Analysis
        ↓
Architecture Planning
        ↓
Backend Engineer
        ↓
Code Review
        ↓
Testing
        ↓
Documentation
```

Frontend and database implementation can therefore be skipped when they are unnecessary.

This is particularly useful when running local LLMs because it reduces unnecessary model inference.

---

## Custom Tools

The agents interact with repositories through custom CrewAI tools.

### CloneRepositoryTool

File:

```text
tools/clone_repository_tool.py
```

Clones a GitHub repository into the local repositories directory.

---

### RepositoryScannerTool

File:

```text
tools/repository_scanner_tool.py
```

Analyzes repository metadata such as:

- Programming language
- Framework
- Package manager
- Entry point
- README availability
- Docker support
- GitHub Actions configuration

---

### CodeSearchTool

File:

```text
tools/code_search_tool.py
```

Searches the repository for:

- Functions
- Classes
- Variables
- Keywords
- Code patterns

and returns matching files.

---

### ReadFileTool

File:

```text
tools/read_file_tool.py
```

Allows agents to read files from the cloned repository.

---

### WriteFileTool

File:

```text
tools/write_file_tool.py
```

Allows implementation agents to create or modify repository files.

---

## Project Structure

```text
software_engineering_team/
│
├── agents/
│   ├── repository_research_analyst.jsonc
│   ├── software_architect.jsonc
│   ├── backend_software_engineer.jsonc
│   ├── frontend_software_engineer.jsonc
│   ├── database_engineer.jsonc
│   ├── senior_code_reviewer.jsonc
│   ├── qa__test_engineer.jsonc
│   └── technical_documentation_specia.jsonc
│
├── knowledge/
│
├── models/
│
├── services/
│   ├── file_service.py
│   ├── repository_service.py
│   ├── scanner_service.py
│   └── search_service.py
│
├── skills/
│
├── tools/
│   ├── clone_repository_tool.py
│   ├── repository_scanner_tool.py
│   ├── code_search_tool.py
│   ├── read_file_tool.py
│   └── write_file_tool.py
│
├── utils/
│   ├── __init__.py
│   └── constants.py
│
├── crew.jsonc
├── flow.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

---

## Technology Stack

- Python
- CrewAI
- CrewAI Flows
- Ollama
- Pydantic
- GitPython
- UV
- Local Large Language Models

---

## Local LLM Support

The project supports local models through Ollama.

An example agent configuration is:

```json
"llm": {
    "model": "qwen2.5-coder:14b",
    "provider": "ollama",
    "base_url": "http://localhost:11434"
}
```

Different Ollama models can be configured depending on available hardware and tool-calling performance.

---

## Installation

### 1. Clone this project

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd software_engineering_team
```

### 2. Install UV

If UV is not already installed, install it using the official UV installation instructions.

Verify:

```bash
uv --version
```

### 3. Install project dependencies

```bash
uv sync
```

---

## Ollama Setup

Install Ollama and verify that it is available:

```bash
ollama --version
```

Pull the model configured in your agents.

For example:

```bash
ollama pull qwen2.5-coder:14b
```

Verify installed models:

```bash
ollama list
```

Make sure Ollama is running before starting the crew.

---

## Running the Crew

The standard CrewAI configuration can be executed using:

```bash
uv run crewai run
```

The project configuration is defined in:

```text
crew.jsonc
```

---

## Running the Conditional Flow

The conditional workflow is implemented in:

```text
flow.py
```

Run it using:

```bash
uv run python flow.py
```

The flow coordinates repository analysis, architecture planning, conditional implementation, review, testing, and documentation.

---

## Example Workflow

Repository:

```text
https://github.com/octocat/Hello-World
```

Example implementation request:

```text
Read README.md and add the line
"Modified by AI Agent for integration testing."
while preserving the existing content.
```

The system analyzes the repository, determines the required implementation path, and allows the appropriate engineering agent to perform the modification using repository tools.

---

## Testing

Individual services and tools can be tested independently using the test scripts included in the project.

Examples include:

```text
test_clone.py
test_code_search.py
test_file_service.py
test_read_file_tool.py
test_repo_scanner.py
test_scanner.py
test_search.py
test_write_file_tool.py
```

Run a test using UV:

```bash
uv run python test_read_file_tool.py
```

---

## Why Local LLMs?

Running agents locally provides several advantages:

- No per-token API charges
- Reduced dependency on third-party model APIs
- Local repository processing
- Ability to experiment with different open models
- Useful environment for studying agent orchestration and tool calling

Local model quality and tool-calling reliability depend heavily on the selected model and available hardware.

---

## Current Limitations

This project is currently an experimental software-engineering agent system rather than a production-ready autonomous developer.

Some limitations include:

- Local models may struggle with complex multi-step tool usage.
- Performance depends heavily on hardware.
- Large repositories can exceed practical local-model context limits.
- Generated code should still be reviewed before being used in production.
- Tool-calling reliability varies between Ollama models.
- The system does not currently provide automatic pull-request creation or deployment.

---

## Future Improvements

Potential future improvements include:

- Git branch creation before modifications
- Git diff generation
- Automated test execution
- Failure-aware retry logic
- Rollback when generated changes fail validation
- Automatic pull-request generation
- Improved architecture-aware routing
- Better repository context management
- Retrieval-based codebase indexing
- Support for larger repositories
- Improved local model tool-calling reliability

---

## Disclaimer

This project is intended for experimentation and learning around multi-agent software engineering systems.

AI-generated code should be reviewed and tested before being merged into production software.