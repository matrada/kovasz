"""Real versioned Copier updates, with no project setup or network access."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml
from copier import run_copy, run_update

ROOT = Path(__file__).resolve().parents[1]


class UpdateTests(unittest.TestCase):
    def git(self, directory, *args):
        return subprocess.run(
            [
                "git",
                "-c",
                "user.name=Template Test",
                "-c",
                "user.email=test@example.invalid",
                "-c",
                "core.hooksPath=/dev/null",
                *args,
            ],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def commit(self, directory):
        self.git(directory, "add", ".")
        self.git(directory, "commit", "-m", "Test fixture")

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        scratch = Path(self.scratch.name)
        self.source = scratch / "template-source"
        shutil.copytree(ROOT / "template", self.source / "template")
        shutil.copy2(ROOT / "copier.yml", self.source / "copier.yml")
        self.git(self.source, "init")
        self.commit(self.source)
        self.git(self.source, "tag", "v1.0.0")
        self.project = scratch / "research-project"
        run_copy(
            str(self.source),
            self.project,
            vcs_ref="v1.0.0",
            defaults=True,
            data={"project_name": "research-project", "author": "Researcher"},
        )
        self.assertFalse((self.project / ".git").exists())
        self.git(self.project, "init")
        self.commit(self.project)

        # A later release changes shared tooling and tries to change/add science.
        config = self.source / "template/pyproject.toml.jinja"
        config.write_text(
            config.read_text().replace("line-length = 88", "line-length = 100")
        )
        makefile = self.source / "template/Makefile.jinja"
        makefile.write_text(makefile.read_text() + "\n# Updated shared tooling\n")
        for name in (
            "README.md.jinja",
            "src/__init__.py",
            "src/new.py",
            "src/nested/new.py",
            "notebooks/new.ipynb",
            "notebooks/experiment.ipynb",
            "data/new.csv",
        ):
            path = self.source / "template" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("New template research content\n")
        self.commit(self.source)
        self.git(self.source, "tag", "v2.0.0")

    def update(self):
        before_head = self.git(self.project, "rev-parse", "HEAD")
        before_refs = self.git(self.project, "show-ref", "--head")
        before_hooks = {
            p.name: p.read_bytes() for p in (self.project / ".git/hooks").iterdir()
        }
        # Any accidentally invoked setup tool fails and leaves evidence.
        trap = Path(self.scratch.name) / "bin"
        trap.mkdir()
        marker = trap / "invoked"
        for name in ("uv", "make", "pre-commit", "jupyter", "ipython"):
            path = trap / name
            path.write_text(f"#!/bin/sh\necho invoked >> '{marker}'\nexit 97\n")
            path.chmod(0o755)
        with patch.dict(
            os.environ, {"PATH": str(trap) + os.pathsep + os.environ["PATH"]}
        ):
            run_update(self.project, vcs_ref="v2.0.0", defaults=True, overwrite=True)
        self.assertFalse(marker.exists())
        self.assertEqual(self.git(self.project, "rev-parse", "HEAD"), before_head)
        self.assertEqual(self.git(self.project, "show-ref", "--head"), before_refs)
        self.assertEqual(
            {p.name: p.read_bytes() for p in (self.project / ".git/hooks").iterdir()},
            before_hooks,
        )
        for name in (".venv", "uv.lock"):
            self.assertFalse((self.project / name).exists())

    def test_version_and_answer_tracking(self):
        answers = yaml.safe_load((self.project / ".copier-answers.yml").read_text())
        self.assertEqual(answers["_commit"], "v1.0.0")
        self.assertEqual(Path(answers["_src_path"]), self.source)
        self.assertEqual(answers["author"], "Researcher")
        self.update()
        answers = yaml.safe_load((self.project / ".copier-answers.yml").read_text())
        self.assertEqual(answers["_commit"], "v2.0.0")
        self.assertEqual(answers["author"], "Researcher")
        self.assertIn(
            "line-length = 100", (self.project / "pyproject.toml").read_text()
        )

    def test_protected_content_and_compatible_configuration(self):
        contents = {
            "README.md": b"# My research\r\nProject-specific README\r\n",
            "src/__init__.py": b"# Research package\n",
            "src/analysis.py": b"def result():\n    return 42\n",
            "notebooks/experiment.ipynb": (
                b'{"cells": [], "metadata": {"study": "mine"}}\n'
            ),
            "data/observations.csv": b"value\n42\n",
        }
        for name, content in contents.items():
            path = self.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        config = self.project / "pyproject.toml"
        config.write_text(
            config.read_text().replace(
                'testpaths = ["tests"]', 'testpaths = ["tests"]\naddopts = "-q"'
            )
        )
        self.commit(self.project)
        self.update()
        for name, content in contents.items():
            self.assertEqual((self.project / name).read_bytes(), content, name)
        for name in (
            "src/new.py",
            "src/nested/new.py",
            "notebooks/new.ipynb",
            "data/new.csv",
        ):
            self.assertFalse((self.project / name).exists(), name)
        self.assertIn("line-length = 100", config.read_text())
        self.assertIn('addopts = "-q"', config.read_text())
        self.assertIn(
            "# Updated shared tooling", (self.project / "Makefile").read_text()
        )
        self.assertEqual(list(self.project.rglob("*.rej")), [])
        self.assertNotIn("<<<<<<<", config.read_text())

    def test_incompatible_configuration_is_visible(self):
        config = self.project / "pyproject.toml"
        config.write_text(
            config.read_text().replace("line-length = 88", "line-length = 120")
        )
        self.commit(self.project)
        self.update()
        conflict = config.read_text()
        self.assertIn("<<<<<<<", conflict)
        self.assertIn("=======", conflict)
        self.assertIn(">>>>>>>", conflict)
        self.assertIn("line-length = 100", conflict)
        self.assertIn("line-length = 120", conflict)
        self.assertIn("pyproject.toml", self.git(self.project, "status", "--short"))

    def test_deleted_project_owned_files_stay_deleted(self):
        for name in ("README.md", "src/__init__.py", "notebooks/.gitkeep"):
            (self.project / name).unlink()
        self.commit(self.project)
        self.update()
        for name in (
            "README.md",
            "src/__init__.py",
            "notebooks/.gitkeep",
            "src/new.py",
            "notebooks/new.ipynb",
        ):
            self.assertFalse((self.project / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
