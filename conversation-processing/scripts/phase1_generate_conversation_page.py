#!/usr/bin/env python3
"""Phase 1: generate a human-readable conversation page for review.

This script reads a raw transcript from conversation-processing/raw-transcripts/
and creates:

- content/blog/conversations/<slug>/index.md
- data/conversations/<slug>.yaml

It does not modify the raw transcript and it does not generate JSON.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from conversation_common import (
    CONVERSATION_DATA_DIR,
    CONVERSATIONS_DIR,
    RAW_TRANSCRIPTS_DIR,
    ConversationError,
    file_sha256,
    parse_exported_transcript,
    project_relative,
    public_conversation_url,
    public_json_url,
    slugify,
    today_iso,
    write_metadata_yaml,
    yaml_list,
    yaml_string,
)


def build_markdown(
    *,
    title: str,
    description: str,
    slug: str,
    source_path: Path,
    turns: list[dict],
    tags: list[str],
    topics: list[str],
) -> str:
    tag_lines = yaml_list(tags, "  ") if tags else ["tags: []"]
    topic_lines = yaml_list(topics, "  ") if topics else ["topics: []"]

    frontmatter_lines = [
        "---",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description)}",
        'type: "post"',
        f"date: {yaml_string(today_iso())}",
        f"lastmod: {yaml_string(today_iso())}",
        "categories:",
        '  - "conversations"',
        *(["tags:"] + tag_lines if tags else tag_lines),
        *(["topics:"] + topic_lines if topics else topic_lines),
        "participants:",
        '  - "Kyle Becker"',
        '  - "Herb"',
        "draft: true",
        f"source_conversation: {yaml_string(project_relative(source_path))}",
        f"canonical_url: {yaml_string(public_conversation_url(slug))}",
        'ai_json: "pending"',
        "---",
        "",
    ]

    body_lines = [
        "<!--",
        "This page was generated from a raw transcript.",
        "Do not edit the raw transcript in conversation-processing/raw-transcripts/.",
        "Review this page before running Phase 2 to generate conversation.json.",
        "-->",
        "",
        "## About This Conversation",
        "",
        description or "TODO: Add a short description before running Phase 2.",
        "",
        "AI-readable JSON: pending",
        "",
        "## Conversation",
        "",
    ]

    for turn in turns:
        body_lines.append(f"### {turn['speaker']} {{#{turn['id']}}}")
        body_lines.append("")
        body_lines.append(turn["content"])
        body_lines.append("")

    return "\n".join(frontmatter_lines + body_lines).rstrip() + "\n"


def build_initial_metadata(
    *,
    title: str,
    description: str,
    slug: str,
    source_path: Path,
    output_path: Path,
    topics: list[str],
    tags: list[str],
) -> dict:
    return {
        "id": slug,
        "title": title,
        "slug": slug,
        "description": description,
        "date": today_iso(),
        "participants": ["Kyle Becker", "Herb"],
        "source_path": project_relative(source_path),
        "source_sha256": file_sha256(source_path),
        "conversation_path": project_relative(output_path),
        "status": "draft",
        "summary": "",
        "canonical_url": public_conversation_url(slug),
        "json_url": public_json_url(slug),
        "topics": topics,
        "keywords": tags,
        "industries": [],
        "concepts": [],
        "audiences": [],
        "key_claims": [],
        "notable_quotes": [],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a draft conversation page and editable metadata."
    )
    parser.add_argument(
        "raw_transcript",
        help=(
            "Raw transcript filename or path. Relative names are resolved from "
            "conversation-processing/raw-transcripts/."
        ),
    )
    parser.add_argument("--slug", help="Conversation slug. Defaults to source filename.")
    parser.add_argument("--title", help="Conversation title. Defaults to title-cased slug.")
    parser.add_argument(
        "--description",
        default="",
        help="Short human-readable description. Can be edited later in metadata YAML.",
    )
    parser.add_argument(
        "--topic",
        action="append",
        default=[],
        help="Canonical topic ID. May be repeated.",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Keyword/tag. May be repeated.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing generated index.md and metadata YAML.",
    )
    return parser.parse_args()


def resolve_raw_path(raw_transcript: str) -> Path:
    candidate = Path(raw_transcript)
    if candidate.is_absolute():
        return candidate
    if candidate.parts and candidate.parts[0] == "conversation-processing":
        return (RAW_TRANSCRIPTS_DIR.parents[1] / candidate).resolve()
    return RAW_TRANSCRIPTS_DIR / raw_transcript


def main() -> int:
    args = parse_args()
    raw_path = resolve_raw_path(args.raw_transcript)
    slug = args.slug or slugify(raw_path.stem)
    title = args.title or slug.replace("-", " ").title()

    output_dir = CONVERSATIONS_DIR / slug
    index_path = output_dir / "index.md"
    metadata_path = CONVERSATION_DATA_DIR / f"{slug}.yaml"

    if not args.overwrite:
        existing = [path for path in [index_path, metadata_path] if path.exists()]
        if existing:
            paths = "\n".join(f"- {project_relative(path)}" for path in existing)
            raise ConversationError(
                "Refusing to overwrite existing generated files. "
                "Use --overwrite if this is intentional:\n" + paths
            )

    turns = parse_exported_transcript(raw_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown = build_markdown(
        title=title,
        description=args.description,
        slug=slug,
        source_path=raw_path,
        turns=turns,
        tags=args.tag,
        topics=args.topic,
    )
    index_path.write_text(markdown, encoding="utf-8")

    metadata = build_initial_metadata(
        title=title,
        description=args.description,
        slug=slug,
        source_path=raw_path,
        output_path=index_path,
        topics=args.topic,
        tags=args.tag,
    )
    write_metadata_yaml(metadata_path, metadata)

    print("Phase 1 complete.")
    print(f"- Wrote {project_relative(index_path)}")
    print(f"- Wrote {project_relative(metadata_path)}")
    print(f"- Parsed {len(turns)} speaker turns")
    print("Review index.md and metadata YAML before running Phase 2.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ConversationError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
