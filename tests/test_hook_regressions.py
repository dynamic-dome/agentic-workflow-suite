import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import date
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_hook(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, REPO_ROOT / "hooks" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PrivateExportGateRegressionTests(unittest.TestCase):
    def test_audit_record_never_persists_sensitive_input_preview(self):
        hook = load_hook("private_export_gate_test", "private-export-gate.py")
        unique_secret = "TOP_SECRET_CARACAL_7f19d2"
        private_path = f"C:/Users/example/private/{unique_secret}.md"

        with tempfile.TemporaryDirectory() as temp_dir:
            hook.LOG_PATH = Path(temp_dir) / "private-export-gate.ndjson"
            event = {
                "tool_name": "mcp__notebooklm__nlm_add_source_text",
                "tool_input": {"source_text": f"{private_path}\npassword={unique_secret}"},
            }
            with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(event))):
                with redirect_stderr(io.StringIO()):
                    self.assertEqual(hook.main(), 0)

            raw_record = hook.LOG_PATH.read_text(encoding="utf-8")
            record = json.loads(raw_record)

        self.assertNotIn(unique_secret.lower(), raw_record.lower())
        self.assertNotIn(private_path.lower(), raw_record.lower())
        self.assertNotIn("haystack_preview", record)
        self.assertEqual(record["decision"], "warn")
        self.assertEqual(record["matched_marker"], "private/")


class WikiCurationCheckRegressionTests(unittest.TestCase):
    def setUp(self):
        self.hook = load_hook("wiki_curation_check_test", "wiki-curation-check.py")
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name) / "configured-wiki-root"
        self.root.mkdir()
        self.hook.WIKI_ROOT = self.root

    def test_logical_relative_target_resolves_under_wiki_root_without_duplicate_segment(self):
        target = self.root / "concepts" / "relative-page.md"
        target.parent.mkdir()
        target.write_text("content without frontmatter\n", encoding="utf-8")
        (self.root / "index.md").write_text("", encoding="utf-8")
        (self.root / "log.md").write_text(date.today().isoformat(), encoding="utf-8")

        unrelated_cwd = Path(self.temp_dir.name) / "invocation-cwd"
        unrelated_cwd.mkdir()
        old_cwd = Path.cwd()
        try:
            os.chdir(unrelated_cwd)
            findings = self.hook.check("wiki/concepts/relative-page.md")
        finally:
            os.chdir(old_cwd)

        self.assertIn("no YAML frontmatter detected", findings)
        self.assertIn("page 'relative-page.md' not linked in wiki/index.md", findings)

    def test_missing_logical_target_returns_explicit_finding(self):
        findings = self.hook.check("wiki/concepts/missing-page.md")
        self.assertEqual(
            findings,
            ["target could not be resolved: wiki/concepts/missing-page.md"],
        )

    def test_unreadable_target_returns_explicit_finding(self):
        target = self.root / "concepts" / "unreadable-page.md"
        target.parent.mkdir()
        target.write_text("---\ntype: concept\n---\n", encoding="utf-8")

        with mock.patch.object(Path, "read_text", side_effect=PermissionError("denied")):
            findings = self.hook.check("wiki/concepts/unreadable-page.md")

        self.assertEqual(
            findings,
            ["target could not be read: wiki/concepts/unreadable-page.md (PermissionError)"],
        )


if __name__ == "__main__":
    unittest.main()
