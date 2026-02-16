import argparse
from pathlib import Path
from ai.llm_client import LLMClient

def read_dir_text(d: Path) -> str:
    chunks = []
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.stat().st_size < 200_000:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            chunks.append(f"\n---\nFILE: {p.relative_to(d)}\n{txt}")
    return "\n".join(chunks).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir", required=True)
    ap.add_argument("--runbooks-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    evidence_dir = Path(args.evidence_dir)
    runbooks_dir = Path(args.runbooks_dir)
    evidence = read_dir_text(evidence_dir)
    runbooks = read_dir_text(runbooks_dir)

    triage_prompt = (
        (Path("ai/prompts/triage.md").read_text(encoding="utf-8")) +
        "\n\nEVIDENCE:\n" + evidence +
        "\n\nRUNBOOKS:\n" + runbooks + "\n"
    )

    llm = LLMClient()
    out = llm.complete(triage_prompt).text

    final = (
        "# AI Incident Triage\n\n"
        "**Guardrails:** Suggestions only. Any prod change requires approval + allowlisted automation.\n\n"
        f"{out}\n\n"
        "## ChatOps commands\n"
        "- `/rollback` (requires approval)\n"
        "- `/generate-tests`\n"
    )
    Path(args.out).write_text(final, encoding="utf-8")

if __name__ == "__main__":
    main()
