"""Formathugun kröfuskjala; engir aukapakkar eða netaðgangur."""

import os
from pathlib import Path
import re
import sys

SECTIONS = (
    "Auðkenni", "Yfirferðar-issue", "Uppruni", "SRS-staðsetning",
    "Gildandi krafa", "Höfundur", "Prófunartilvik",
)
FIELDS = (
    "Krafa", "Tegund", "Forsendur og upphafsástand",
    "Aðgerð eða inntak", "Vænt niðurstaða",
)
ID = re.compile(r"[^\W_][\w.-]*", re.UNICODE)
ISSUE = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/issues/[1-9][0-9]*(?=$|[\s)#])")


def blocks(text, level):
    """Return (heading, body, line) for exact-level Markdown headings."""
    headings = list(re.finditer(r"^" + "#" * level + r" (.+?)\s*$", text, re.M))
    return [
        (match[1], text[match.end():headings[i + 1].start() if i + 1 < len(headings) else len(text)].strip(),
         text.count("\n", 0, match.start()) + 1)
        for i, match in enumerate(headings)
    ]


def filled(value):
    return bool(value.strip()) and value.strip() not in {"...", "…", "-"}


def check(root):
    """Return errors (relative file, line, message) and number of documents."""
    root = Path(root)
    errors = []
    req_ids, test_ids = set(), set()
    directory = root / "requirements"
    if not directory.is_dir():
        return [("requirements", 1, "Kröfumöppuna requirements/ vantar.")], 0
    files = sorted(p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() == ".md"
                   and p != directory / "FR-XX.md")
    for path in files:
        name = path.relative_to(root).as_posix()

        def error(message, line=1):
            errors.append((name, line, message))

        try:
            text = path.read_text(encoding="utf-8-sig")
        except (UnicodeError, OSError):
            error("Ekki tókst að lesa skrána sem UTF-8.")
            continue
        # Comments are instructions, not document content. Preserve line numbers.
        text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
        placeholder = re.search(r"<(?!https?://)[^>]+>", text)
        if placeholder:
            error("Skiptið <...> leiðbeiningareitum út fyrir eigið efni.", text.count("\n", 0, placeholder.start()) + 1)
        sections = {}
        for heading, body, line in blocks(text, 2):
            if heading in sections:
                error(f"Kaflinn '{heading}' kemur oftar en einu sinni fyrir.", line)
            sections[heading] = (body, line)
        for heading in SECTIONS:
            if heading not in sections or not filled(sections[heading][0]):
                error(f"Kaflann '## {heading}' vantar eða hann er tómur.", sections.get(heading, ("", 1))[1])

        def body(heading):
            return sections.get(heading, ("", 1))[0]

        req_id = body("Auðkenni")
        if not ID.fullmatch(req_id) or req_id != path.stem:
            error("Auðkenni skal vera eitt stöðugt auðkenni, eins og skráarnafnið án .md.")
        if req_id in req_ids:
            error(f"Auðkennið '{req_id}' er notað í fleiri en einni skrá.")
        req_ids.add(req_id)
        if not ISSUE.search(body("Yfirferðar-issue")):
            error("Yfirferðar-issue þarf heilan https://github.com/eigandi/safn/issues/númer tengil.")
        srs_links = re.findall(r"\]\(([^)]+)\)", body("SRS-staðsetning"))
        if not any((path.parent / link.split("#")[0]).resolve() == (root / "SRS-yfirlit.md").resolve()
                   for link in srs_links) or not (root / "SRS-yfirlit.md").is_file():
            error("SRS-staðsetning þarf tengil í fyrirliggjandi SRS-yfirlit.md.")
        tests = blocks(body("Prófunartilvik"), 3)
        if not tests:
            error("Skráið að minnsta kosti eitt prófunartilvik með ### <auðkenni prófs>.")
        for test_id, content, _ in tests:
            if not ID.fullmatch(test_id):
                error(f"Prófunarauðkennið '{test_id}' þarf að vera eitt stöðugt auðkenni.")
            if test_id in test_ids:
                error(f"Prófunarauðkennið '{test_id}' er notað oftar en einu sinni.")
            test_ids.add(test_id)
            fields = {}
            # Each field may span several lines, up to the next field.
            matches = list(re.finditer(r"^\*\*(.+?):\*\*[ \t]*(.*)$", content, re.M))
            for i, match in enumerate(matches):
                value = content[match.start(2):matches[i + 1].start() if i + 1 < len(matches) else len(content)].strip()
                if match[1] in fields:
                    error(f"Próf {test_id}: reiturinn '{match[1]}' er tvítekinn.")
                fields[match[1]] = value
            for field in FIELDS:
                if not filled(fields.get(field, "")):
                    error(f"Próf {test_id}: reitinn '**{field}:**' vantar eða hann er tómur.")
            if fields.get("Krafa") != req_id:
                error(f"Próf {test_id}: reiturinn 'Krafa' þarf að vera '{req_id}'.")
            if fields.get("Tegund") not in {"venjulegt", "undantekning", "jaðartilvik"}:
                error(f"Próf {test_id}: Tegund þarf að vera venjulegt, undantekning eða jaðartilvik.")
    return errors, len(files)


def escape(value):
    return str(value).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A").replace(",", "%2C").replace(":", "%3A")


def main():
    errors, count = check(Path(__file__).resolve().parent.parent)
    for path, line, message in errors:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::error file={escape(path)},line={line}::{escape(message)}")
        else:
            print(f"{path}:{line}: {message}")
    if errors:
        print(f"Formathugun mistókst: {len(errors)} frávik í {count} kröfuskjölum.")
        return 1
    print(f"Formathugun stóðst: {count} kröfuskjöl." if count else
          "Engin útfyllt kröfuskjöl enn; aðeins sniðmát. Þetta er ekki mat á skilum.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
