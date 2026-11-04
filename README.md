# kovász

A notebook-first geospatial research template with one complete Python toolbox.

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and
Make. Generate a project from the public template or a local clone:

```bash
uv tool install copier
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

These focused checks generate a fresh project and verify file-only generation,
empty research scaffolding, and directory-based data tracking. To check the full
environment, follow the quick start against a local clone and run `make check`.

## License

MIT
