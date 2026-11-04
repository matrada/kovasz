# kovász

A notebook-first geospatial research template with one complete Python toolbox.

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and
Make. Generate a project from the public template or a local clone:

```bash
uv tool install "copier>=9.19.1"
copier copy gh:matyasrada/kovasz my-project
# Or, from a local development clone:
# copier copy --vcs-ref HEAD path/to/kovasz my-project
cd my-project
```

The local-development command selects `HEAD` to use the clone's current commit;
without it, Copier selects the latest release tag. The public command uses the
latest release.

Copier asks for a lowercase **project_name**, a short **description**, and an
**author**. Generation only writes project files and `.copier-answers.yml`.
Inspect them, then explicitly initialize Git before setup:

```bash
git init
make init
make check
git add .
git commit -m "Initialize research project"
```

`make init` installs the full research environment into `.venv`, creates a
trackable `uv.lock`, and installs Git hooks (Ruff, Ruff format, and nbstripout).
Repeat it whenever needed. No command creates a Git commit automatically.
Configure your Git name and email if needed before committing.

Kernel registration is optional and separate:

```bash
make kernel
uv run jupyter lab
```

Select **Python (my-project)** (or your chosen project name). `make kernel`
registers that name in your Jupyter user data directory; override it with
`make kernel KERNEL_NAME=another-name` for multiple checkouts.

## Research workspace

`notebooks/` and `src/` begin as empty scaffolding. The generated README describes
the workflow, and `make check` runs Ruff lint, formatting checks, and a geospatial
import smoke test. `make test` runs only tests.

Data and generated results belong in ignored directories such as `data/`,
`inputs/`, `outputs/`, and `reports/`. Formats are not blanket-ignored: small CSV
or GeoJSON fixtures under `tests/fixtures/` can be tracked.

## Updating an existing project

The refreshed template supports ongoing updates with Copier 9.19.1 or newer.
Keep `.copier-answers.yml` tracked: it records the source, template version, and
answers needed to update. Generate from a release tag (Copier's default) for a
versioned starting point. For local development, commit and tag a disposable
local template copy and use `copier copy --vcs-ref <tag> <source> <destination>`.

After generation, `README.md`, `notebooks/`, `src/`, and `data/` are project-owned.
Updates exclude these complete paths, preserving your contents and intentional
deletions, and do not add new template files there. Keep reusable research code
in `src/` and notebooks in `notebooks/`. Other shared files, including
`pyproject.toml`, `Makefile`, hooks configuration, and template smoke tests,
continue to receive improvements. You can customize shared configuration;
compatible edits merge, while overlapping incompatible edits need manual review.

Start from a clean Git worktree with your research committed. From the generated
project directory:

```bash
git status --short
copier update --defaults
# Or select a particular later release:
# copier update --defaults --vcs-ref <tag>
git diff --stat
git diff
git status --short
```

Review all changes, including `.copier-answers.yml`. Copier's default inline
conflicts contain `<<<<<<<`, `=======`, and `>>>>>>>` markers; resolve each one
before using the configuration. If you select Copier's reject-file conflict
mode instead, inspect and resolve every `.rej` file. An update can finish with
conflicts, so command success alone does not establish that the result is ready.

Updating only changes files; it does not set up the project environment or create
a project commit. After resolving conflicts and reviewing dependency/tooling
changes, explicitly run `make init` to sync the full environment, refresh
`uv.lock`, and reinstall hooks, then `make check`. Review and commit the lockfile
and adopted changes yourself. Run `make kernel` separately only if you want to
register or refresh the optional Jupyter kernel.

This update contract applies to projects generated with the refreshed template's
ownership rules. Projects generated from older Kovász releases are individual
migration cases: there is no automatic migration promise. Review their answers,
existing setup tasks, research ownership, and configuration against a newly
generated project before deciding what to adopt; do not assume a direct update
will preserve their research or avoid old setup tasks.

## Comes with

**tools** — uv, ruff, pytest, pre-commit, nbstripout, jupyterlab, ipykernel

**geospatial stack** — xarray, rioxarray, rasterio, geopandas, pyproj

**storage** — zarr, netcdf4, h5netcdf, h5py, virtualizarr

**stac/odc** — pystac, pystac-client, odc-stac, odc-geo, odc-loader

**cloud** — boto3, s3fs, obstore

**compute** — dask, distributed, jax

**ml** — scikit-learn, mlflow

**viz** — matplotlib, cartopy, lonboard

## Template checks

```bash
uv run --with copier python -m unittest discover -s tests -v
```

These checks verify file-only generation, empty research scaffolding, and
directory-based data tracking. They also create disposable local Git templates
with two release tags and exercise real Copier updates, exact research-content
preservation, shared configuration merges/conflicts, and absence of setup side
effects. To check the full
environment, follow the quick start against a local clone and run `make check`.

## License

MIT
