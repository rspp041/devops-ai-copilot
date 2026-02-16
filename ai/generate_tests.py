import argparse
from pathlib import Path
from ai.llm_client import LLMClient

def load_prompt(repo_root: Path, name: str) -> str:
    return (repo_root / "ai" / "prompts" / name).read_text(encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", required=True, help="Path to unified diff")
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--service", required=True, help="Service directory (e.g., apps/sample-service)")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    repo_root = Path(args.repo_root)
    diff_text = Path(args.diff).read_text(encoding="utf-8", errors="ignore")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    p_plan = load_prompt(repo_root, "test_plan.md")
    p_gen  = load_prompt(repo_root, "test_gen.md")

    llm = LLMClient()

    plan_prompt = f"{p_plan}\n\nPR DIFF:\n{diff_text}\n"
    plan_md = llm.complete(plan_prompt).text

    report = (
        "# AI Test Generation Report\n\n"
        "## Proposed Test Plan\n\n"
        f"{plan_md}\n\n"
        "## Output\n"
        "- Generated tests are written to the service under `tests/test_generated_ai.py`\n"
    )
    (out_dir / "REPORT.md").write_text(report, encoding="utf-8")

    service_dir = repo_root / args.service
    test_path = service_dir / "tests" / "test_generated_ai.py"
    test_path.parent.mkdir(parents=True, exist_ok=True)

    gen_prompt = (
        f"{p_gen}\n\n"
        "Context:\n"
        f"- Target file path: {test_path.as_posix()}\n\n"
        f"PR DIFF:\n{diff_text}\n"
    )
    code = llm.complete(gen_prompt).text.strip()

    if "def test_" not in code:
        code = (
            "import pytest\n\n"
            "# AI could not confidently generate tests from the diff.\n"
            "# Add targeted unit tests here.\n\n"
            "def test_placeholder():\n"
            "    assert True\n"
        )

    test_path.write_text(code + "\n", encoding="utf-8")
    (service_dir / "AI_TEST_REPORT.md").write_text(report, encoding="utf-8")

if __name__ == "__main__":
    main()
