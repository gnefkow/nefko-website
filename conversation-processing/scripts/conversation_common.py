#!/usr/bin/env python3
"""Shared helpers for the conversation publishing scripts.

These helpers intentionally use only the Python standard library so the
conversation workflow does not depend on a package install step.
"""

from __future__ import annotations

import json
import re
import hashlib
from datetime import date
from pathlib import Path
from typing import Any


SITE_ROOT = Path(__file__).resolve().parents[2]
RAW_TRANSCRIPTS_DIR = SITE_ROOT / "conversation-processing" / "raw-transcripts"
CONVERSATIONS_DIR = SITE_ROOT / "content" / "blog" / "conversations"
CONVERSATION_DATA_DIR = SITE_ROOT / "data" / "conversations"
AI_INDEX_DIR = SITE_ROOT / "static" / "ai"
AI_TOPICS_DIR = AI_INDEX_DIR / "topics"
BASE_URL = "https://nefko.xyz"

SPEAKER_MAP = {
    "Cursor": "Herb",
    "User": "Kyle",
}


class ConversationError(Exception):
    """Raised when a conversation file cannot be processed safely."""


def slugify(value: str) -> str:
    """Create a conservative URL slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "conversation"


def public_conversation_url(slug: str) -> str:
    return f"{BASE_URL}/blog/conversations/{slug}/"


def public_json_url(slug: str) -> str:
    return f"{public_conversation_url(slug)}conversation.json"


def project_relative(path: Path) -> str:
    return path.relative_to(SITE_ROOT).as_posix()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_outer_blank_lines(lines: list[str]) -> list[str]:
    """Remove blank wrapper lines without changing content lines."""
    start = 0
    end = len(lines)
    while start < end and lines[start] == "":
        start += 1
    while end > start and lines[end - 1] == "":
        end -= 1
    return lines[start:end]


def parse_exported_transcript(raw_path: Path) -> list[dict[str, Any]]:
    """Parse a Cursor-style exported conversation without editing turn text."""
    if not raw_path.exists():
        raise ConversationError(f"Raw transcript not found: {raw_path}")

    raw_text = raw_path.read_text(encoding="utf-8")
    turns: list[dict[str, Any]] = []
    current_speaker: str | None = None
    current_lines: list[str] = []

    speaker_pattern = re.compile(r"^\*\*(.+?)\*\*\s*$")

    def flush_turn() -> None:
        nonlocal current_speaker, current_lines
        if current_speaker is None:
            current_lines = []
            return

        lines = strip_outer_blank_lines(current_lines)
        if lines:
            turn_number = len(turns) + 1
            exported_speaker = current_speaker
            public_speaker = SPEAKER_MAP.get(exported_speaker, exported_speaker)
            turns.append(
                {
                    "id": f"turn-{turn_number:03d}",
                    "speaker": public_speaker,
                    "exported_speaker": exported_speaker,
                    "content": "\n".join(lines),
                }
            )
        current_lines = []

    for line in raw_text.splitlines():
        match = speaker_pattern.match(line)
        if match:
            flush_turn()
            current_speaker = match.group(1).strip()
            continue

        if current_speaker is None:
            continue

        if line.strip() == "---":
            continue

        current_lines.append(line)

    flush_turn()

    if not turns:
        raise ConversationError(
            f"No speaker turns found in {project_relative(raw_path)}. "
            "Expected speaker lines like **Cursor** and **User**."
        )

    return turns


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values: list[str], indent: str = "") -> list[str]:
    if not values:
        return [f"{indent}[]"]
    return [f"{indent}- {yaml_string(value)}" for value in values]


def write_metadata_yaml(path: Path, metadata: dict[str, Any]) -> None:
    """Write a simple YAML file that is easy for humans and scripts to edit."""
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    scalar_fields = [
        "id",
        "title",
        "slug",
        "description",
        "date",
        "participants",
        "source_path",
        "source_sha256",
        "conversation_path",
        "status",
        "summary",
        "canonical_url",
        "json_url",
    ]
    list_fields = [
        "topics",
        "keywords",
        "industries",
        "concepts",
        "audiences",
        "key_claims",
        "notable_quotes",
        "best_for_queries",
    ]

    for field in scalar_fields:
        value = metadata.get(field, "")
        if isinstance(value, list):
            lines.append(f"{field}:")
            lines.extend(yaml_list([str(item) for item in value], "  "))
        else:
            lines.append(f"{field}: {yaml_string(str(value))}")

    for field in list_fields:
        lines.append(f"{field}:")
        values = metadata.get(field, [])
        lines.extend(yaml_list([str(item) for item in values], "  "))

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    """Parse the constrained YAML shape written by write_metadata_yaml."""
    if not path.exists():
        raise ConversationError(f"Metadata file not found: {path}")

    result: dict[str, Any] = {}
    current_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            if value == "":
                result[current_key] = []
            elif value == "[]":
                result[current_key] = []
            else:
                result[current_key] = parse_yaml_scalar(value)
            continue

        if current_key and line.startswith("  - "):
            item = parse_yaml_scalar(line[4:].strip())
            result.setdefault(current_key, [])
            if not isinstance(result[current_key], list):
                raise ConversationError(f"Mixed scalar/list field in {path}: {current_key}")
            result[current_key].append(item)

    return result


def parse_yaml_scalar(value: str) -> str:
    if value.startswith('"') and value.endswith('"'):
        try:
            parsed = json.loads(value)
            return str(parsed)
        except json.JSONDecodeError:
            return value.strip('"')
    return value


def read_frontmatter(markdown_path: Path) -> tuple[dict[str, Any], str]:
    text = markdown_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ConversationError(f"Markdown file has no YAML frontmatter: {markdown_path}")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ConversationError(f"Markdown frontmatter is not closed: {markdown_path}")

    frontmatter_text = text[4:end]
    body = text[end + 5 :]

    temp_path = markdown_path.with_suffix(markdown_path.suffix + ".frontmatter.tmp")
    try:
        temp_path.write_text(frontmatter_text + "\n", encoding="utf-8")
        frontmatter = parse_simple_yaml(temp_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()

    return frontmatter, body


def write_frontmatter(frontmatter: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                lines.extend(yaml_list([str(item) for item in value], "  "))
            else:
                lines.append(f"{key}: []")
        else:
            lines.append(f"{key}: {yaml_string(str(value))}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip("\n")


def parse_markdown_turns(markdown_path: Path) -> list[dict[str, str]]:
    """Read generated transcript turns from headings in index.md."""
    _, body = read_frontmatter(markdown_path)
    heading_pattern = re.compile(r"^### (.+?) \{#(turn-\d{3})\}\s*$")

    turns: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current, current_lines
        if current is None:
            current_lines = []
            return
        current["content"] = "\n".join(strip_outer_blank_lines(current_lines))
        turns.append(current)
        current = None
        current_lines = []

    for line in body.splitlines():
        match = heading_pattern.match(line)
        if match:
            flush()
            current = {"speaker": match.group(1), "id": match.group(2), "content": ""}
            continue

        if current is not None:
            current_lines.append(line)

    flush()

    if not turns:
        raise ConversationError(f"No generated transcript turns found in {markdown_path}")

    return turns


def today_iso() -> str:
    return date.today().isoformat()
