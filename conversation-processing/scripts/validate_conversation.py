#!/usr/bin/env python3
"""Validate generated conversation outputs.

This script does not generate content. It checks that the generated page,
metadata, JSON payload, and discovery indexes are internally consistent.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from conversation_common import (
    AI_INDEX_DIR,
    CONVERSATION_DATA_DIR,
    CONVERSATIONS_DIR,
    RAW_TRANSCRIPTS_DIR,
    SITE_ROOT,
    ConversationError,
    file_sha256,
    parse_markdown_turns,
    parse_simple_yaml,
    project_relative,
    public_conversation_url,
    public_json_url,
    read_frontmatter,
)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return SITE_ROOT / path


def validate_slug(slug: str, *, require_json: bool) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    conversation_dir = CONVERSATIONS_DIR / slug
    index_path = conversation_dir / "index.md"
    json_path = conversation_dir / "conversation.json"
    metadata_path = CONVERSATION_DATA_DIR / f"{slug}.yaml"

    require(index_path.exists(), f"Missing {project_relative(index_path)}", errors)
    require(metadata_path.exists(), f"Missing {project_relative(metadata_path)}", errors)
    if require_json:
        require(json_path.exists(), f"Missing {project_relative(json_path)}", errors)

    if errors:
        return errors

    metadata = parse_simple_yaml(metadata_path)
    frontmatter, body = read_frontmatter(index_path)
    turns = parse_markdown_turns(index_path)

    source_path_value = str(metadata.get("source_path", ""))
    require(bool(source_path_value), "Metadata is missing source_path", errors)
    raw_path = resolve_project_path(source_path_value) if source_path_value else RAW_TRANSCRIPTS_DIR
    require(raw_path.exists(), f"Raw transcript not found: {source_path_value}", errors)

    if raw_path.exists() and metadata.get("source_sha256"):
        current_hash = file_sha256(raw_path)
        require(
            current_hash == metadata.get("source_sha256"),
            "Raw transcript hash changed since Phase 1. "
            "Regenerate from the reviewed source before publishing.",
            errors,
        )

    expected_canonical = public_conversation_url(slug)
    expected_json = public_json_url(slug)

    require(
        str(frontmatter.get("canonical_url", "")) == expected_canonical,
        f"index.md canonical_url should be {expected_canonical}",
        errors,
    )

    if json_path.exists():
        payload: dict[str, Any] = json.loads(json_path.read_text(encoding="utf-8"))
        require(payload.get("id") == slug, "conversation.json id does not match slug", errors)
        require(
            payload.get("canonical_url") == expected_canonical,
            f"conversation.json canonical_url should be {expected_canonical}",
            errors,
        )
        require(
            payload.get("json_url") == expected_json,
            f"conversation.json json_url should be {expected_json}",
            errors,
        )
        require(
            frontmatter.get("ai_json") == expected_json,
            f"index.md ai_json should be {expected_json}",
            errors,
        )
        require(
            expected_json in body,
            "index.md body should visibly link to conversation.json after Phase 2",
            errors,
        )
        require(
            payload.get("conversation_turns") == turns,
            "conversation.json turns do not match index.md turns. Regenerate Phase 2.",
            errors,
        )
    elif "pending" not in str(frontmatter.get("ai_json", "")):
        warnings.append("conversation.json is missing, but ai_json is not marked pending.")

    for field in ["title", "description", "summary"]:
        if not metadata.get(field):
            warnings.append(f"Metadata field is empty: {field}")

    for field in ["topics", "keywords"]:
        value = metadata.get(field, [])
        if not value:
            warnings.append(f"Metadata list is empty: {field}")

    if json_path.exists():
        ai_index_path = AI_INDEX_DIR / "index.json"
        require(ai_index_path.exists(), "Missing static/ai/index.json", errors)
        if ai_index_path.exists():
            ai_index = json.loads(ai_index_path.read_text(encoding="utf-8"))
            resources = ai_index.get("resources", [])
            require(
                any(resource.get("id") == slug for resource in resources),
                "static/ai/index.json does not include this conversation",
                errors,
            )

    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    return errors


def validate_build_outputs(slug: str) -> list[str]:
    """Validate local Hugo build outputs after the site has been built."""
    errors: list[str] = []
    public_dir = SITE_ROOT / "public"
    sitemap_path = public_dir / "sitemap.xml"
    human_page_path = public_dir / "blog" / "conversations" / slug / "index.html"
    json_payload_path = public_dir / "blog" / "conversations" / slug / "conversation.json"
    ai_index_path = public_dir / "ai" / "index.json"

    expected_canonical = public_conversation_url(slug)
    expected_json = public_json_url(slug)

    require(public_dir.exists(), "Missing public/ build directory. Run the Hugo build first.", errors)
    require(human_page_path.exists(), f"Built human page missing: {project_relative(human_page_path)}", errors)
    require(json_payload_path.exists(), f"Built JSON payload missing: {project_relative(json_payload_path)}", errors)
    require(ai_index_path.exists(), f"Built AI index missing: {project_relative(ai_index_path)}", errors)
    require(sitemap_path.exists(), f"Built sitemap missing: {project_relative(sitemap_path)}", errors)

    if sitemap_path.exists():
        sitemap = sitemap_path.read_text(encoding="utf-8")
        require(
            expected_canonical in sitemap,
            f"sitemap.xml does not include {expected_canonical}",
            errors,
        )

    if human_page_path.exists():
        html = human_page_path.read_text(encoding="utf-8")
        require(
            expected_json in html,
            f"Built human page does not link to {expected_json}",
            errors,
        )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated conversation files.")
    parser.add_argument("slug", help="Conversation slug under content/blog/conversations/.")
    parser.add_argument(
        "--require-json",
        action="store_true",
        help="Fail if conversation.json and AI indexes do not exist.",
    )
    parser.add_argument(
        "--check-build",
        action="store_true",
        help="Also validate public/ build outputs and sitemap inclusion.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_slug(args.slug, require_json=args.require_json)
    if args.check_build:
        errors.extend(validate_build_outputs(args.slug))
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Validation passed for {args.slug}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ConversationError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
