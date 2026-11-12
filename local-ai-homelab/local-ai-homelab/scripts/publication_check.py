"""Limited publication hygiene check; not a substitute for full-history secret scanning."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "private IPv4": re.compile(r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"),
    "GPU UUID": re.compile(r"GPU-[0-9a-fA-F]{8}-[0-9a-fA-F-]{20,}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
}


def main():
    failures = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(p in {".git", "__pycache__", ".venv"} for p in path.relative_to(ROOT).parts):
            continue
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            failures.append((path.relative_to(ROOT), "local environment file present"))
            continue
        if path.suffix in {".py", ".md", ".yaml", ".yml", ".example"} or path.name == ".gitignore":
            content = path.read_text(encoding="utf-8")
            failures.extend((path.relative_to(ROOT), label) for label, rule in RULES.items() if rule.search(content))
    for path, label in failures:
        print(f"Review {path}: {label}")  # Never print matched sensitive values.
    print(f"Publication heuristic: {len(failures)} finding(s). Manual review still required.")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
