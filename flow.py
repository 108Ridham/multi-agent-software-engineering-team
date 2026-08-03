"""
Conditional multi-agent software engineering pipeline using CrewAI Flows.

Workflow
--------
1. repository_analysis   – Repository Research Analyst scans the repo.
2. architecture_planning – Software Architect plans the work and decides
                           which specialist engineers are needed.
3. implementation        – Only the required engineers run (backend /
                           frontend / database — any combination).
4. code_review           – Senior Code Reviewer reviews all implementations.
5. testing               – QA & Test Engineer validates the changes.
6. documentation         – Technical Documentation Specialist writes the docs.

Task names are resolved dynamically from crew.jsonc — no hardcoded indices.
"""

from __future__ import annotations

from typing import Dict, List

from crewai.flow.flow import Flow, listen, start
from crewai.project.crew_loader import load_crew
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Task name constants — match the "name" fields in crew.jsonc
# ---------------------------------------------------------------------------
TASK_REPOSITORY_ANALYSIS    = "repository_analysis"
TASK_ARCHITECTURE_PLANNING  = "architecture_planning"
TASK_BACKEND_IMPLEMENTATION = "backend_implementation"
TASK_FRONTEND_IMPLEMENTATION= "frontend_implementation"
TASK_DATABASE_IMPLEMENTATION= "database_implementation"
TASK_CODE_REVIEW            = "code_review"
TASK_TESTING                = "testing"
TASK_DOCUMENTATION          = "documentation"


# ---------------------------------------------------------------------------
# Flow state
# ---------------------------------------------------------------------------
class SoftwareEngineeringState(BaseModel):
    repository_url: str = ""
    implementation_request: str = ""

    repository_report: str = ""
    architecture_plan: str = ""

    needs_backend: bool = False
    needs_frontend: bool = False
    needs_database: bool = False

    implementation_reports: List[str] = []
    code_review_report: str = ""
    testing_report: str = ""
    final_documentation: str = ""


# ---------------------------------------------------------------------------
# Helper – build a name→task index map from the loaded crew
# ---------------------------------------------------------------------------
def _task_index_map() -> Dict[str, int]:
    """Return {task_name: position} for the crew defined in crew.jsonc."""
    crew, _ = load_crew("crew.jsonc")
    return {task.name: idx for idx, task in enumerate(crew.tasks)}


# ---------------------------------------------------------------------------
# Helper – run a subset of tasks from the shared crew
# ---------------------------------------------------------------------------
def _run_tasks(task_names: List[str], inputs: dict) -> str:
    """
    Load the crew, resolve task names to positions, restrict to that subset,
    and kick off.  Task names must match the "name" fields in crew.jsonc.
    """
    crew, default_inputs = load_crew("crew.jsonc")
    all_tasks = crew.tasks

    # Build name→task object map
    name_to_task = {task.name: task for task in all_tasks}

    # Preserve crew.jsonc order while selecting only the requested tasks
    selected = [name_to_task[n] for n in task_names if n in name_to_task]

    if not selected:
        raise ValueError(f"None of the requested task names found in crew: {task_names}")

    crew.tasks = selected
    result = crew.kickoff(inputs={**default_inputs, **inputs})

    # Restore original task list
    crew.tasks = all_tasks
    return str(result)


# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------
def _detect_needs(architecture_plan: str) -> dict:
    """
    Parse the Software Architect's plan to decide which engineers are needed.

    The heuristic looks for explicit mentions of backend / frontend / database
    work in the plan.  This keeps the routing free of an extra LLM call.
    """
    text = architecture_plan.lower()

    backend_keywords = [
        "backend", "back-end", "api", "server", "endpoint", "route",
        "controller", "service", "middleware", "rest", "graphql",
    ]
    frontend_keywords = [
        "frontend", "front-end", "ui", "interface", "component",
        "html", "css", "javascript", "react", "vue", "angular",
        "template", "view", "page",
    ]
    database_keywords = [
        "database", "db", "schema", "migration", "model", "query",
        "sql", "nosql", "mongo", "postgres", "mysql", "orm",
        "table", "index", "seed",
    ]

    needs_backend = any(kw in text for kw in backend_keywords)
    needs_frontend = any(kw in text for kw in frontend_keywords)
    needs_database = any(kw in text for kw in database_keywords)

    # Fallback: if nothing matched, run at least the backend engineer
    if not needs_backend and not needs_frontend and not needs_database:
        needs_backend = True

    return {
        "needs_backend": needs_backend,
        "needs_frontend": needs_frontend,
        "needs_database": needs_database,
    }


# ---------------------------------------------------------------------------
# Flow definition
# ---------------------------------------------------------------------------
class SoftwareEngineeringFlow(Flow[SoftwareEngineeringState]):

    # ------------------------------------------------------------------
    # Step 1 – entry point
    # ------------------------------------------------------------------
    @start()
    def receive_request(self):
        print("\n=== SOFTWARE ENGINEERING FLOW STARTED ===")
        print(f"Repository : {self.state.repository_url}")
        print(f"Request    : {self.state.implementation_request}")
        return self.state.implementation_request

    # ------------------------------------------------------------------
    # Step 2 – Repository Research Analyst
    # ------------------------------------------------------------------
    @listen(receive_request)
    def repository_analysis(self, _):
        print("\n=== [1/6] REPOSITORY ANALYSIS ===")

        inputs = {
            "repository_url": self.state.repository_url,
            "implementation_request": self.state.implementation_request,
        }
        result = _run_tasks([TASK_REPOSITORY_ANALYSIS], inputs)
        self.state.repository_report = result

        print("Repository analysis complete.")
        return result

    # ------------------------------------------------------------------
    # Step 3 – Software Architect
    # ------------------------------------------------------------------
    @listen(repository_analysis)
    def architecture_planning(self, repository_report):
        print("\n=== [2/6] ARCHITECTURE PLANNING ===")

        inputs = {
            "repository_url": self.state.repository_url,
            "implementation_request": self.state.implementation_request,
            "repository_report": repository_report,
        }
        result = _run_tasks([TASK_REPOSITORY_ANALYSIS, TASK_ARCHITECTURE_PLANNING], inputs)
        self.state.architecture_plan = result

        # Determine which engineers are needed based on the plan
        needs = _detect_needs(result)
        self.state.needs_backend = needs["needs_backend"]
        self.state.needs_frontend = needs["needs_frontend"]
        self.state.needs_database = needs["needs_database"]

        print(
            f"Architecture planning complete.\n"
            f"  Backend  needed: {self.state.needs_backend}\n"
            f"  Frontend needed: {self.state.needs_frontend}\n"
            f"  Database needed: {self.state.needs_database}"
        )
        return result

    # ------------------------------------------------------------------
    # Step 4 – Conditional implementation (only required engineers run)
    # ------------------------------------------------------------------
    @listen(architecture_planning)
    def implementation(self, _):
        print("\n=== [3/6] CONDITIONAL IMPLEMENTATION ===")

        # Build the minimal task list for this request
        impl_tasks = [TASK_REPOSITORY_ANALYSIS, TASK_ARCHITECTURE_PLANNING]

        if self.state.needs_backend:
            print("  → Running Backend Engineer")
            impl_tasks.append(TASK_BACKEND_IMPLEMENTATION)

        if self.state.needs_frontend:
            print("  → Running Frontend Engineer")
            impl_tasks.append(TASK_FRONTEND_IMPLEMENTATION)

        if self.state.needs_database:
            print("  → Running Database Engineer")
            impl_tasks.append(TASK_DATABASE_IMPLEMENTATION)

        inputs = {
            "repository_url": self.state.repository_url,
            "implementation_request": self.state.implementation_request,
        }
        result = _run_tasks(impl_tasks, inputs)
        self.state.implementation_reports.append(result)

        print("Implementation complete.")
        return result

    # ------------------------------------------------------------------
    # Step 5 – Senior Code Reviewer
    # ------------------------------------------------------------------
    @listen(implementation)
    def code_review(self, implementation_result):
        print("\n=== [4/6] CODE REVIEW ===")

        # code_review in crew.jsonc has context on all three implementation
        # tasks.  Include only the tasks that actually ran so CrewAI can
        # resolve context references without errors.
        review_tasks = [
            TASK_REPOSITORY_ANALYSIS,
            TASK_ARCHITECTURE_PLANNING,
        ]
        if self.state.needs_backend:
            review_tasks.append(TASK_BACKEND_IMPLEMENTATION)
        if self.state.needs_frontend:
            review_tasks.append(TASK_FRONTEND_IMPLEMENTATION)
        if self.state.needs_database:
            review_tasks.append(TASK_DATABASE_IMPLEMENTATION)
        review_tasks.append(TASK_CODE_REVIEW)

        inputs = {
            "repository_url": self.state.repository_url,
            "implementation_request": self.state.implementation_request,
        }
        result = _run_tasks(review_tasks, inputs)
        self.state.code_review_report = result

        print("Code review complete.")
        return result

    # ------------------------------------------------------------------
    # Step 6 – QA & Test Engineer
    # ------------------------------------------------------------------
    @listen(code_review)
    def testing(self, code_review_result):
        print("\n=== [5/6] TESTING ===")

        test_tasks = [
            TASK_REPOSITORY_ANALYSIS,
            TASK_ARCHITECTURE_PLANNING,
        ]
        if self.state.needs_backend:
            test_tasks.append(TASK_BACKEND_IMPLEMENTATION)
        if self.state.needs_frontend:
            test_tasks.append(TASK_FRONTEND_IMPLEMENTATION)
        if self.state.needs_database:
            test_tasks.append(TASK_DATABASE_IMPLEMENTATION)
        test_tasks += [TASK_CODE_REVIEW, TASK_TESTING]

        inputs = {
            "repository_url": self.state.repository_url,
            "implementation_request": self.state.implementation_request,
        }
        result = _run_tasks(test_tasks, inputs)
        self.state.testing_report = result

        print("Testing complete.")
        return result

    # ------------------------------------------------------------------
    # Step 7 – Technical Documentation Specialist
    # ------------------------------------------------------------------
    @listen(testing)
    def documentation(self, testing_result):
        print("\n=== [6/6] DOCUMENTATION ===")

        doc_tasks = [
            TASK_REPOSITORY_ANALYSIS,
            TASK_ARCHITECTURE_PLANNING,
        ]
        if self.state.needs_backend:
            doc_tasks.append(TASK_BACKEND_IMPLEMENTATION)
        if self.state.needs_frontend:
            doc_tasks.append(TASK_FRONTEND_IMPLEMENTATION)
        if self.state.needs_database:
            doc_tasks.append(TASK_DATABASE_IMPLEMENTATION)
        doc_tasks += [TASK_CODE_REVIEW, TASK_TESTING, TASK_DOCUMENTATION]

        inputs = {
            "repository_url": self.state.repository_url,
            "implementation_request": self.state.implementation_request,
        }
        result = _run_tasks(doc_tasks, inputs)
        self.state.final_documentation = result

        print("\n=== FLOW COMPLETED ===")
        print(
            f"Agents used:\n"
            f"  Repository Research Analyst : ✓\n"
            f"  Software Architect          : ✓\n"
            f"  Backend Engineer            : {'✓' if self.state.needs_backend else '✗ (skipped)'}\n"
            f"  Frontend Engineer           : {'✓' if self.state.needs_frontend else '✗ (skipped)'}\n"
            f"  Database Engineer           : {'✓' if self.state.needs_database else '✗ (skipped)'}\n"
            f"  Senior Code Reviewer        : ✓\n"
            f"  QA & Test Engineer          : ✓\n"
            f"  Technical Documentation     : ✓"
        )
        return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    print("=== MULTI-AGENT SOFTWARE ENGINEERING FLOW ===")
    print()

    repository_url = input("GitHub repository URL: ").strip()
    if not repository_url:
        raise SystemExit("Error: repository URL cannot be empty.")

    print()
    print("Describe the implementation request (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    implementation_request = "\n".join(lines).strip()

    if not implementation_request:
        raise SystemExit("Error: implementation request cannot be empty.")

    flow = SoftwareEngineeringFlow()

    result = flow.kickoff(
        inputs={
            "repository_url": repository_url,
            "implementation_request": implementation_request,
        }
    )

    print("\n=== FINAL OUTPUT ===")
    print(result)