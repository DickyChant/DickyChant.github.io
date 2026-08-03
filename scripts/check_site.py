#!/usr/bin/env python3
"""Small, dependency-free checks for the generated Hugo site."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.images = 0
        self.images_without_alt = 0
        self.json_blocks: list[str] = []
        self._json_parts: list[str] | None = None

    def handle_starttag(
        self, tag: str, attrs_list: list[tuple[str, str | None]]
    ) -> None:
        attrs = dict(attrs_list)
        element_id = attrs.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)

        if tag == "a" and attrs.get("href"):
            self.references.append(("href", attrs["href"]))
        if tag in {"img", "script"} and attrs.get("src"):
            self.references.append(("src", attrs["src"]))
        if tag == "link" and attrs.get("href"):
            self.references.append(("href", attrs["href"]))

        if tag == "img":
            self.images += 1
            if "alt" not in attrs:
                self.images_without_alt += 1

        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_parts is not None:
            self.json_blocks.append("".join(self._json_parts))
            self._json_parts = None

    def handle_data(self, data: str) -> None:
        if self._json_parts is not None:
            self._json_parts.append(data)


def resolve_local(root: Path, page: Path, reference: str) -> tuple[Path, str] | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None

    path_text = unquote(parsed.path)
    if not path_text:
        return page, parsed.fragment

    if path_text.startswith("/"):
        target = root / path_text.lstrip("/")
    else:
        target = page.parent / path_text

    if path_text.endswith("/"):
        target /= "index.html"
    elif not target.suffix and target.is_dir():
        target /= "index.html"

    return target.resolve(), parsed.fragment


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    pages = sorted(root.rglob("*.html"))
    if not pages:
        raise SystemExit(f"No HTML pages found under {root}")

    audits: dict[Path, PageAudit] = {}
    errors: list[str] = []
    image_count = 0

    for page in pages:
        audit = PageAudit()
        audit.feed(page.read_text(encoding="utf-8"))
        audit.close()
        audits[page.resolve()] = audit
        image_count += audit.images

        if audit.duplicate_ids:
            errors.append(f"{page}: duplicate IDs {sorted(audit.duplicate_ids)}")
        if audit.images_without_alt:
            errors.append(f"{page}: {audit.images_without_alt} image(s) missing alt")
        for block in audit.json_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{page}: invalid JSON-LD ({exc})")

    for page, audit in audits.items():
        for kind, reference in audit.references:
            resolved = resolve_local(root, page, reference)
            if resolved is None:
                continue
            target, fragment = resolved
            if not target.exists():
                errors.append(f"{page}: broken {kind} {reference!r}")
                continue
            if fragment and target.suffix == ".html":
                target_audit = audits.get(target)
                if target_audit and fragment not in target_audit.ids:
                    errors.append(f"{page}: missing fragment {reference!r}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(
        f"Validated {len(pages)} HTML pages, {image_count} image elements, "
        "local references, fragments, IDs, alt attributes, and JSON-LD."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
