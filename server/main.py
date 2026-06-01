"""Wolfgang Rush — Indian Property & Conveyancing Drafting MCPB.

Local-execution.

License: MIT
Source: https://github.com/Wolfgangrush/indian-property-drafting-mcpb
Privacy policy: https://wolfgangrush.github.io/privacy/
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

DEFAULT_DRAFTS_ROOT = Path.home() / "Downloads" / "Wolfgang-Rush-Drafts"
ALLOWED_ARTIFACT_NAMES = {
    "case-facts.md",
    "format-shell.md",
    "draft-v1.md",
    "draft-v1.docx",
    "verification-report.md",
    "draft-v2.md",
    "draft-v2.docx",
    "opposing-notes.md",
    "final-draft.md",
}

mcp = FastMCP("wolfgang-indian-property-drafting")

BUNDLE_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = BUNDLE_ROOT / "skills"
AGENTS_DIR = BUNDLE_ROOT / "agents"
PLEADING_BASE_DIR = SKILLS_DIR / "_property_drafting_base"
STATE_CONFIG_DIR = BUNDLE_ROOT / "state-config" / "exemplars"

CASE_TYPES: list[str] = [
    "gift-deed",
    "mortgage-deed",
    "partition-deed",
    "settlement-deed",
    "exchange-deed",
    "release-deed",
    "easement-deed",
    "wakf-deed",
    "private-trust-deed",
    "title-investigation-report",
]

CASE_TYPE_DESCRIPTIONS: dict[str, str] = {
    "gift-deed": "Gift deed under Section 122 Transfer of Property Act 1882",
    "mortgage-deed": "Mortgage deed (English / simple / equitable) under Sections 58-104 TPA",
    "partition-deed": "Partition deed for co-owned / ancestral / joint family property",
    "settlement-deed": "Settlement deed under Section 17 Registration Act",
    "exchange-deed": "Exchange deed under Section 118 TPA",
    "release-deed": "Release deed / relinquishment instrument",
    "easement-deed": "Easement deed under the Indian Easements Act 1882",
    "wakf-deed": "Wakf deed under the Wakf Act 1995",
    "private-trust-deed": "Private trust deed under the Indian Trusts Act 1882",
    "title-investigation-report": "Title-investigation report (advocate's certificate of title)",
}

AGENT_NAMES: list[str] = ["reader", "format", "drafter", "verifier", "refiner", "overseer"]




ACRONYM_TO_CASE_TYPE: dict[str, str] = {}


FULL_ORCHESTRATION_SCRIPT = """# WOLFGANG RUSH — INDIAN CIVIL COURTS (PROPERTY SUITS, PARTITION, DECLARATION, POSSESSION) DRAFTING · FULL ORCHESTRATION SCRIPT

**YOU MUST execute every step below in order. DO NOT skip steps. DO NOT write
standalone python-docx, JavaScript, or shell scripts to generate output —
invoke the tools listed at each step.**

## STEP 0 — CREATE THE CASE FOLDER

Call `create_case_folder(case_type)` where `case_type` is one of:
gift-deed, mortgage-deed, partition-deed, settlement-deed, exchange-deed, release-deed, easement-deed, wakf-deed, private-trust-deed, title-investigation-report.

The tool returns `case_folder` — an absolute path. **Use this path in every
subsequent save_artifact and save_draft_as_docx call.**

## STEP 1 — MATERIALIZE THE USER'S INPUT DOCUMENTS

Every source document the user attached to this conversation must be saved to
disk before the Reader can run. For each attachment:

Call `save_artifact(case_folder, "inputs/source-document.txt", <extracted-text>)`

## STEP 2 — LOAD THE CASE-TYPE SKILL

Call `get_case_type_format(case_type)`. Read the returned SKILL.md carefully.

## STEP 3 — LOAD THE PLEADING BASE

Call `get_pleading_base()`. Read the universal skeleton + common drafting
discipline (citation rules, AI-fabricated-citation risk per HC cautions).

## STEP 4 — RUN THE READER AGENT (APPLIES PRIVACY FIREWALL)

Call `get_agent_instructions("reader")` to load the Reader persona. The Reader
applies the privacy firewall — substitutes party names, addresses, identifying
numbers, financial figures, statutory-notice references with structural
placeholders BEFORE any downstream agent processes the facts.

Save the output via `save_artifact(case_folder, "case-facts.md", <content>)`.

## STEP 5 — RUN THE FORMAT AGENT

Call `get_agent_instructions("format")`. Map case-facts.md (already privacy-
firewalled) into the SKILL.md placeholders.

Save via `save_artifact(case_folder, "format-shell.md", <content>)`.

## STEP 6 — RUN THE DRAFTER AGENT

Call `get_agent_instructions("drafter")`. Write the first complete draft using
format-shell.md as scaffold and case-facts.md as ground-truth.

Save markdown via `save_artifact(case_folder, "draft-v1.md", <content>)`. Then
`save_draft_as_docx(<markdown>, f"{case_folder}/draft-v1.docx")`.

## STEP 7 — RUN THE VERIFIER AGENT (ANTI-HALLUCINATION FIREWALL — DO NOT SKIP)

Call `get_agent_instructions("verifier")`. Compare draft-v1.md against
case-facts.md fact-by-fact. Flag every hallucinated date, fabricated citation,
unsupported assertion, orphan annexure marker, missing factual basis.

Save via `save_artifact(case_folder, "verification-report.md", <content>)`.

## STEP 8 — RUN THE REFINER AGENT

Call `get_agent_instructions("refiner")`. Apply every Verifier flag. Polish
language. Enforce Registry formatting.

Save via `save_artifact(case_folder, "draft-v2.md", <content>)` and
`save_draft_as_docx(<markdown>, f"{case_folder}/draft-v2.docx")`.

## STEP 9 — RUN THE OVERSEER AGENT (OPPOSING-COUNSEL LENS — DO NOT SKIP)

Call `get_agent_instructions("overseer")`. Read draft-v2.md with opposing-
counsel lens. Find weak prayers, contradictory facts, attackable defects.

Save via `save_artifact(case_folder, "opposing-notes.md", <content>)`. Then
apply hardening to produce final draft. Save via
`save_artifact(case_folder, "final-draft.md", <content>)` and
`save_draft_as_docx(<markdown>, f"{case_folder}/final-draft.docx")`.

## STEP 10 — REPORT TO THE USER

Return the absolute path to `final-draft.docx` and a one-paragraph summary.

---

**FALSIFICATION CHECK:** the case folder must contain at minimum:
1. case-facts.md
2. format-shell.md
3. draft-v1.docx (or draft-v1.md)
4. verification-report.md
5. draft-v2.docx (or draft-v2.md)
6. final-draft.docx

If any are missing, return to the matching STEP and produce it.

**REMINDER:** YOU MUST NOT write a standalone python-docx generator, a
JavaScript script, or any one-shot drafting program. The MCPB exposes every
required tool. Use them.
"""


@mcp.tool(annotations=ToolAnnotations(title="Get Pipeline Agent Instructions", readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def get_agent_instructions(agent_name: str = "") -> str:
    """Get the instructions for the drafting pipeline.

    Default mode (no agent_name, or agent_name=""): returns the FULL orchestration
    script enumerating every step and tool call from case-folder creation through
    final-draft.docx. THIS IS THE MANDATORY FIRST CALL when the user asks you to
    draft anything.

    Single-agent mode (agent_name ∈ {reader, format, drafter, verifier, refiner,
    overseer}): returns that agent's persona instructions only.
    """
    if not agent_name or agent_name == "full":
        return FULL_ORCHESTRATION_SCRIPT
    if agent_name not in AGENT_NAMES:
        return (
            f"Error: unknown agent_name '{agent_name}'. "
            f"Available: {', '.join(AGENT_NAMES)}. "
            "Call with no arguments to receive the full orchestration script."
        )
    agent_md = AGENTS_DIR / agent_name / f"{agent_name}.md"
    if not agent_md.exists():
        return f"Error: agent file not found for '{agent_name}'."
    return agent_md.read_text(encoding="utf-8")


@mcp.tool(annotations=ToolAnnotations(title="Get Pleading Base Structure", readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def get_pleading_base() -> str:
    """Get the shared property drafting base structure."""
    common_md = SKILLS_DIR / "_drafting_common" / "SKILL.md"
    parts: list[str] = []
    if PLEADING_BASE_DIR.exists():
        for md_file in sorted(PLEADING_BASE_DIR.glob("*.md")):
            parts.extend([f"# {md_file.stem}", "", md_file.read_text(encoding="utf-8"), "", "---", ""])
    if common_md.exists():
        parts.extend(["# Common Drafting Discipline", "", common_md.read_text(encoding="utf-8")])
    return "\n".join(parts)


def _list_states_internal() -> list[str]:
    if not STATE_CONFIG_DIR.exists():
        return []
    return sorted(p.stem for p in STATE_CONFIG_DIR.iterdir() if p.is_file() and p.suffix == ".md" and not p.name.startswith("_"))


@mcp.tool(annotations=ToolAnnotations(title="List Available State Exemplars", readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def list_states() -> dict:
    """List the State exemplars available for property drafting."""
    states = _list_states_internal()
    return {"states": states, "count": len(states), "note": "Call get_state_exemplar(state) for the per-State content."}


@mcp.tool(annotations=ToolAnnotations(title="Get State-Specific Exemplar Content", readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def get_state_exemplar(state: str) -> str:
    """Get the State-specific exemplar.

    Args:
        state: Lowercase hyphenated state name. Use list_states() to discover.
    """
    available = _list_states_internal()
    if state not in available:
        return f"Error: no exemplar found for state '{state}'. Available: {', '.join(available)}."
    exemplar_path = STATE_CONFIG_DIR / f"{state}.md"
    if not exemplar_path.exists():
        return f"Error: exemplar file missing for state '{state}'."
    return exemplar_path.read_text(encoding="utf-8")


@mcp.tool(annotations=ToolAnnotations(title="Read Case Folder Files", readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def read_case_folder(path: str) -> dict:
    """Read all files in a case folder.

    Args:
        path: Absolute or relative path to the case folder.
    """
    folder = Path(path).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        return {"error": f"Path '{path}' is not a valid directory.", "files": {}, "warnings": [], "file_count": 0}
    files: dict[str, str] = {}
    warnings: list[str] = []
    for f in sorted(folder.rglob("*")):
        if not f.is_file() or any(p.startswith(".") for p in f.relative_to(folder).parts):
            continue
        rel = f.relative_to(folder).as_posix()
        ext = f.suffix.lower()
        try:
            if ext in (".md", ".txt"):
                files[rel] = f.read_text(encoding="utf-8", errors="replace")
            elif ext == ".pdf":
                try:
                    r = subprocess.run(["pdftotext", str(f), "-"], capture_output=True, text=True, timeout=30)
                    files[rel] = r.stdout if r.returncode == 0 else f"[PDF at {rel} — extract failed]"
                    if r.returncode != 0:
                        warnings.append(f"pdftotext failed on {rel}")
                except FileNotFoundError:
                    warnings.append("pdftotext not installed")
                    files[rel] = f"[PDF at {rel} — pdftotext not installed]"
                except subprocess.TimeoutExpired:
                    warnings.append(f"pdftotext timed out on {rel}")
            elif ext == ".docx":
                try:
                    r = subprocess.run(["pandoc", "-f", "docx", "-t", "markdown", str(f)], capture_output=True, text=True, timeout=30)
                    files[rel] = r.stdout if r.returncode == 0 else f"[DOCX at {rel} — extract failed]"
                    if r.returncode != 0:
                        warnings.append(f"pandoc failed on {rel}")
                except FileNotFoundError:
                    warnings.append("pandoc not installed")
                    files[rel] = f"[DOCX at {rel} — pandoc not installed]"
                except subprocess.TimeoutExpired:
                    warnings.append(f"pandoc timed out on {rel}")
            else:
                warnings.append(f"Skipped unsupported file type: {rel}")
        except Exception as exc:
            warnings.append(f"Error reading {rel}: {exc}")
    return {"folder": str(folder), "files": files, "warnings": warnings, "file_count": len(files)}


@mcp.tool(annotations=ToolAnnotations(title="Save Draft as Filing-Grade DOCX", readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def save_draft_as_docx(markdown_text: str, output_path: str) -> dict:
    """Save markdown draft as filing-grade .docx using pandoc.

    Args:
        markdown_text: Draft content in markdown.
        output_path: Where to save the .docx file.
    """
    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    reference_docx = PLEADING_BASE_DIR / "reference.docx" if (PLEADING_BASE_DIR / "reference.docx").exists() else None
    temp_md = output.parent / f".{output.stem}.tmp.md"
    temp_md.write_text(markdown_text, encoding="utf-8")
    cmd = ["pandoc", str(temp_md), "-o", str(output)]
    if reference_docx:
        cmd.extend(["--reference-doc", str(reference_docx)])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        temp_md.unlink(missing_ok=True)
        if r.returncode != 0:
            return {"success": False, "error": r.stderr.strip()[:500], "output_path": str(output)}
        return {"success": True, "output_path": str(output), "file_size_bytes": output.stat().st_size, "reference_docx_applied": reference_docx is not None}
    except FileNotFoundError:
        temp_md.unlink(missing_ok=True)
        return {"success": False, "error": "pandoc not installed.", "output_path": str(output)}
    except subprocess.TimeoutExpired:
        temp_md.unlink(missing_ok=True)
        return {"success": False, "error": "pandoc conversion timed out after 60s.", "output_path": str(output)}


def _sanitise_path_component(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]", "-", value.strip())
    cleaned = cleaned.strip(".-_") or "untitled"
    return cleaned[:80]


@mcp.tool(annotations=ToolAnnotations(title="Create Case Folder", readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=False))
def create_case_folder(case_type: str, base_dir: str = "") -> dict:
    """Create the case folder for a drafting session on the user's machine.

    Creates a timestamped folder under ~/Downloads/Wolfgang-Rush-Drafts/ (or the
    base_dir if supplied) named <case-type>-<YYYYMMDD-HHMMSS>/, with an inputs/
    subfolder for source documents. Cross-platform (macOS / Windows / Linux).
    """
    if case_type not in CASE_TYPES:
        return {"error": f"unknown case_type '{case_type}'. Available: {', '.join(CASE_TYPES)}."}
    parent = Path(base_dir).expanduser().resolve() if base_dir else DEFAULT_DRAFTS_ROOT
    parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder_name = f"{_sanitise_path_component(case_type)}-{timestamp}"
    case_folder = parent / folder_name
    inputs_folder = case_folder / "inputs"
    inputs_folder.mkdir(parents=True, exist_ok=True)
    readme = case_folder / "README.md"
    readme.write_text(
        f"# Wolfgang Rush Drafting Case Folder\n\n"
        f"- Case type: {case_type}\n"
        f"- Created: {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"## Artifacts (pipeline output)\n"
        f"- `inputs/` — source documents\n"
        f"- `case-facts.md` — Reader output (privacy-firewalled)\n"
        f"- `format-shell.md` — Format output\n"
        f"- `draft-v1.docx` — Drafter output\n"
        f"- `verification-report.md` — Verifier output\n"
        f"- `draft-v2.docx` — Refiner output\n"
        f"- `opposing-notes.md` — Overseer output\n"
        f"- `final-draft.docx` — Final filing-grade output\n",
        encoding="utf-8",
    )
    return {
        "case_folder": str(case_folder),
        "inputs_folder": str(inputs_folder),
        "case_type": case_type,
        "timestamp": timestamp,
        "next_step": (
            "Save every source document the user attached to this conversation "
            f"into '{inputs_folder}' via save_artifact, then proceed to STEP 2 "
            "of the orchestration script (get_case_type_format)."
        ),
    }


@mcp.tool(annotations=ToolAnnotations(title="Save Pipeline Artifact", readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False))
def save_artifact(case_folder: str, relative_path: str, content: str) -> dict:
    """Save a pipeline artifact or input document into the case folder.

    Required at the end of every agent step. Pipeline artifact names accepted at
    the root: case-facts.md, format-shell.md, draft-v1.md, draft-v1.docx,
    verification-report.md, draft-v2.md, draft-v2.docx, opposing-notes.md,
    final-draft.md. Input documents go under inputs/ (e.g.,
    'inputs/source-document.txt').
    """
    case_dir = Path(case_folder).expanduser().resolve()
    if not case_dir.exists() or not case_dir.is_dir():
        return {"success": False, "error": f"case_folder '{case_folder}' does not exist. Call create_case_folder first."}
    rel = Path(relative_path)
    if rel.is_absolute():
        return {"success": False, "error": "relative_path must not be absolute."}
    if any(part == ".." for part in rel.parts):
        return {"success": False, "error": "relative_path must not contain '..'."}
    is_root_artifact = len(rel.parts) == 1
    if is_root_artifact and rel.name not in ALLOWED_ARTIFACT_NAMES:
        return {"success": False, "error": f"'{rel.name}' is not a recognised root-level artifact. Allowed: {', '.join(sorted(ALLOWED_ARTIFACT_NAMES))}. Input documents must go under inputs/."}
    target = (case_dir / rel).resolve()
    try:
        target.relative_to(case_dir)
    except ValueError:
        return {"success": False, "error": "resolved path escapes the case_folder."}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"success": True, "path": str(target), "file_size_bytes": target.stat().st_size, "relative_path": rel.as_posix()}


if __name__ == "__main__":
    mcp.run()
