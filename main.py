from __future__ import annotations

from pathlib import Path
from typing import Any


def define_env(env: Any) -> None:
    project_dir = Path(env.project_dir)

    def _docs_dir() -> Path:
        candidates = []
        for config_obj in (getattr(env, "conf", None), getattr(env, "config", None), env.variables.get("config")):
            if config_obj is None:
                continue
            if isinstance(config_obj, dict) and config_obj.get("docs_dir"):
                candidates.append(config_obj["docs_dir"])
            else:
                docs_dir = getattr(config_obj, "docs_dir", None)
                if docs_dir:
                    candidates.append(docs_dir)
        docs_dir = next((value for value in candidates if value), "docs")
        return project_dir / str(docs_dir)

    docs_dir = _docs_dir()

    def _current_page_path(page: Any) -> Path | None:
        if page is None:
            return None
        file_obj = getattr(page, "file", None)
        if file_obj is None:
            return None

        abs_src_path = getattr(file_obj, "abs_src_path", None)
        if abs_src_path:
            return Path(abs_src_path)

        for attr in ("src_uri", "src_path"):
            rel = getattr(file_obj, attr, None)
            if rel:
                return docs_dir / str(rel)
        return None

    def _extract_title(path: Path) -> str:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return path.stem.replace("-", " ").replace("_", " ").title()

    def _strip_frontmatter(text: str) -> str:
        if not text.startswith("---\n"):
            return text
        parts = text.split("\n---\n", 1)
        return parts[1] if len(parts) == 2 else text

    def _extract_summary(path: Path) -> str:
        text = _strip_frontmatter(path.read_text(encoding="utf-8"))
        lines = text.splitlines()
        after_title = False
        paragraph: list[str] = []

        for raw_line in lines:
            line = raw_line.strip()

            if not after_title:
                if line.startswith("# "):
                    after_title = True
                continue

            if not line:
                if paragraph:
                    break
                continue

            if line.startswith("#"):
                if paragraph:
                    break
                continue

            if line.startswith("{{") or line.startswith("{%"):
                continue

            if line.startswith("- ") or line.startswith("* "):
                if paragraph:
                    break
                continue

            paragraph.append(line)

        return " ".join(paragraph)

    @env.macro
    def list_matching_pages(
        pattern: str,
        page: Any = None,
        base_dir: str | None = None,
        exclude: str | None = None,
        summaries: bool = False,
    ) -> str:
        current_page = _current_page_path(page)
        if base_dir is not None:
            directory = (docs_dir / base_dir).resolve()
        elif current_page is not None:
            directory = current_page.parent.resolve()
        else:
            raise ValueError("list_matching_pages requires either page=page or base_dir='...'")

        current_page_resolved = current_page.resolve() if current_page is not None else None
        exclude_patterns = [part.strip() for part in (exclude or "").split(",") if part.strip()]
        matches = []
        for candidate in sorted(directory.glob(pattern)):
            if not candidate.is_file() or candidate.suffix != ".md":
                continue
            if candidate.name.startswith("."):
                continue
            if current_page_resolved is not None and candidate.resolve() == current_page_resolved:
                continue
            if exclude_patterns and any(candidate.match(glob) for glob in exclude_patterns):
                continue
            matches.append(candidate)

        if not matches:
            return "_No matching documents._"

        lines = []
        for candidate in matches:
            title = _extract_title(candidate)
            if summaries:
                summary = _extract_summary(candidate)
                if summary:
                    lines.append(f"- [{title}]({candidate.name}) - {summary}")
                    continue
            lines.append(f"- [{title}]({candidate.name})")
        return "\n".join(lines)

    @env.macro
    def list_project_workflow_sections(page: Any = None, summaries: bool = True) -> str:
        current_page = _current_page_path(page)
        if current_page is None:
            raise ValueError("list_project_workflow_sections requires page=page")

        project_dir = current_page.parent.resolve()
        candidates = []
        for subdir in sorted(project_dir.iterdir()):
            if not subdir.is_dir():
                continue

            index_candidates = [
                subdir / "README.md",
                subdir / f"{subdir.name.split('-', 1)[-1].upper()}.md",
                subdir / f"{subdir.name.split('-', 1)[-1].upper()}.en.md",
                subdir / f"{subdir.name.split('-', 1)[-1].upper()}.pl.md",
            ]

            index_path = next((path for path in index_candidates if path.exists()), None)
            if index_path is None:
                md_files = sorted(
                    path for path in subdir.glob("*.md") if path.is_file() and not path.name.startswith(".")
                )
                index_path = md_files[0] if md_files else None

            if index_path is None:
                continue

            candidates.append(index_path)

        if not candidates:
            return "_No workflow sections found._"

        lines = []
        for candidate in candidates:
            rel = candidate.relative_to(project_dir)
            title = _extract_title(candidate)
            if summaries:
                summary = _extract_summary(candidate)
                if summary:
                    lines.append(f"- [{title}]({rel.as_posix()}) - {summary}")
                    continue
            lines.append(f"- [{title}]({rel.as_posix()})")
        return "\n".join(lines)
