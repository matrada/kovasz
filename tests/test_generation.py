"""File generation and Git tracking policy, without environment setup."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from copier import run_copy

ROOT = Path(__file__).resolve().parents[1]


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        scratch = Path(self.scratch.name)
        # Use the source files, including changes not yet committed.
        source = scratch / "template-source"
        shutil.copytree(ROOT / "template", source / "template")
        shutil.copy2(ROOT / "copier.yml", source / "copier.yml")
        self.project = scratch / "research-project"
        run_copy(
            str(source),
            self.project,
            defaults=True,
            data={"project_name": "research-project"},
        )

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.project, capture_output=True, text=True, check=True
        )

    def test_generation_only_writes_files(self):
        self.assertTrue((self.project / ".copier-answers.yml").is_file())
        for name in (".git", ".venv", "uv.lock"):
            self.assertFalse((self.project / name).exists(), name)
        # Any setup task, even one writing outside the project, needs trust.
        # run_copy above succeeds with unsafe=False (the default).
        self.assertIn("make init", (self.project / "README.md").read_text())
        self.assertIn("research-project", (self.project / "Makefile").read_text())

    def test_empty_research_scaffolding(self):
        self.assertEqual(
            list((self.project / "notebooks").iterdir()),
            [self.project / "notebooks/.gitkeep"],
        )
        self.assertEqual(
            list((self.project / "src").iterdir()), [self.project / "src/__init__.py"]
        )
        self.assertEqual((self.project / "src/__init__.py").read_text(), "")
        self.assertEqual(list(self.project.rglob("*.ipynb")), [])

    def test_directory_data_policy_and_trackable_lock(self):
        self.git("init")
        for name in (
            "data",
            "reports",
            "inputs",
            "outputs",
            "tmp",
            "cache",
            "raw",
            "processed",
            "scratch",
        ):
            path = self.project / name / "sample.csv"
            path.parent.mkdir()
            path.write_text("value\n1\n")
            self.assertEqual(
                self.git("check-ignore", str(path)).stdout.strip(), str(path)
            )
        fixtures = self.project / "tests/fixtures"
        fixtures.mkdir()
        (fixtures / "sample.csv").write_text("value\n1\n")
        (fixtures / "sample.geojson").write_text(
            '{"type":"FeatureCollection","features":[]}\n'
        )
        (self.project / "uv.lock").write_text("version = 1\n")
        self.git("add", "tests/fixtures", "uv.lock")
        self.assertEqual(
            set(self.git("diff", "--cached", "--name-only").stdout.splitlines()),
            {"tests/fixtures/sample.csv", "tests/fixtures/sample.geojson", "uv.lock"},
        )


if __name__ == "__main__":
    unittest.main()
