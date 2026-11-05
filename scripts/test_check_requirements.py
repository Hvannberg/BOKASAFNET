"""Regression tests for format validation, not student acceptance tests."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from check_requirements import check

VALID = """# FR-3 – Sækja skjal

## Auðkenni
FR-3
## Yfirferðar-issue
https://github.com/group/project/issues/3
## Uppruni
FR-3, https://github.com/group/original/issues/1
## SRS-staðsetning
3.1 Skjöl – [Yfirlit](../SRS-yfirlit.md)
## Gildandi krafa
Kerfið skal birta valið skjal þegar notandi velur það.
## Höfundur
Anna Jónsdóttir
## Prófunartilvik
### PT-3-1
**Krafa:** FR-3
**Tegund:** venjulegt
**Forsendur og upphafsástand:** Skjal er til; notandi hefur aðgang.
**Aðgerð eða inntak:** Notandi velur skjalið.
**Vænt niðurstaða:** Kerfið birtir valið skjal.
"""


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "requirements").mkdir()
        (self.root / "SRS-yfirlit.md").write_text("# SRS", encoding="utf-8")

    def write(self, text=VALID, name="FR-3.md"):
        (self.root / "requirements" / name).write_text(text, encoding="utf-8")

    def messages(self):
        return "\n".join(message for _, _, message in check(self.root)[0])

    def test_valid_and_preserved_identifier(self):
        self.write()
        self.assertEqual(check(self.root), ([], 1))

    def test_template_is_excluded(self):
        self.write("<unfilled template>", "FR-XX.md")
        self.assertEqual(check(self.root), ([], 0))

    def test_actual_template_copy_needs_filling(self):
        template = Path(__file__).resolve().parent.parent / "requirements/FR-XX.md"
        self.write(template.read_text(encoding="utf-8"))
        self.assertIn("leiðbeiningareitum", self.messages())

    def test_missing_and_empty_sections(self):
        for text in (VALID.replace("## Höfundur", "## Annað"), VALID.replace("Anna Jónsdóttir", "")):
            with self.subTest(text=text):
                self.write(text)
                self.assertIn("Höfundur", self.messages())

    def test_mismatched_filename(self):
        self.write(name="FR-4.md")
        self.assertIn("skráarnafnið", self.messages())

    def test_issue_link_required(self):
        self.write(VALID.replace("https://github.com/group/project/issues/3", "#3"))
        self.assertIn("Yfirferðar-issue þarf", self.messages())

    def test_srs_link_and_file_required(self):
        self.write(VALID.replace("../SRS-yfirlit.md", "../other.md"))
        self.assertIn("SRS-staðsetning þarf", self.messages())
        self.write()
        (self.root / "SRS-yfirlit.md").unlink()
        self.assertIn("SRS-staðsetning þarf", self.messages())

    def test_missing_tests(self):
        self.write(VALID.split("### PT-3-1")[0])
        self.assertIn("að minnsta kosti eitt prófunartilvik", self.messages())

    def test_missing_test_field_and_wrong_reference(self):
        self.write(VALID.replace("**Vænt niðurstaða:** Kerfið birtir valið skjal.", "").replace("**Krafa:** FR-3", "**Krafa:** FR-4"))
        self.assertIn("Vænt niðurstaða", self.messages())
        self.assertIn("þarf að vera 'FR-3'", self.messages())

    def test_duplicate_test_ids_across_requirements(self):
        self.write()
        self.write(VALID.replace("FR-3", "FR-4"), "FR-4.md")
        self.assertIn("notað oftar en einu sinni", self.messages())

    def test_duplicate_requirement_ids(self):
        self.write()
        (self.root / "requirements/sub").mkdir()
        self.write(VALID.replace("../SRS", "../../SRS"), "sub/FR-3.md")
        self.assertIn("fleiri en einni skrá", self.messages())

    def test_tbd_and_multiline_fields_are_allowed(self):
        self.write(VALID.replace("Kerfið birtir valið skjal.", "TBD, sjá eftirfylgni í issue.\nNæsta lína."))
        self.assertEqual(check(self.root), ([], 1))

    def test_missing_requirements_directory(self):
        (self.root / "requirements").rmdir()
        self.assertIn("Kröfumöppuna", self.messages())

    def test_invalid_utf8(self):
        (self.root / "requirements/FR-3.md").write_bytes(b"\xff")
        self.assertIn("UTF-8", self.messages())

    def run_cli(self, github=False):
        scripts = self.root / "scripts"
        scripts.mkdir(exist_ok=True)
        checker = Path(__file__).with_name("check_requirements.py")
        shutil.copy2(checker, scripts / checker.name)
        env = dict(os.environ, PYTHONUTF8="1", GITHUB_ACTIONS="true" if github else "false")
        return subprocess.run(
            [sys.executable, str(scripts / checker.name)],
            cwd=self.root, env=env, capture_output=True, encoding="utf-8",
        )

    def test_cli_success_exit_code(self):
        self.write()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Formathugun stóðst: 1", result.stdout)

    def test_cli_failure_and_github_annotation(self):
        self.write(VALID.replace("**Vænt niðurstaða:** Kerfið birtir valið skjal.", ""))
        result = self.run_cli(github=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("::error file=requirements/FR-3.md,line=", result.stdout)
        self.assertIn("Vænt niðurstaða", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_failure_then_fix_in_same_file(self):
        self.write(VALID.replace("**Krafa:** FR-3", "**Krafa:** FR-4"))
        self.assertEqual(self.run_cli().returncode, 1)
        self.write()
        self.assertEqual(self.run_cli().returncode, 0)


if __name__ == "__main__":
    unittest.main()
