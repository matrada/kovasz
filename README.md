# kovász

minimal geospatial data science template

## quick start

```bash
uv tool install copier
mkdir -p my-project && copier copy --trust gh:matyasrada/kovasz my-project
```

or from a local clone:

```bash
mkdir -p my-project && copier copy --trust path/to/kovasz my-project
```

## prompts

- **project_name** — lowercase, hyphens ok
- **description** — one-liner
- **author** — name

## on `copier copy`, kovasz:

1. runs **uv sync**, which installs deps and writes a committed `uv.lock`
2. registers a **jupyter kernel** named after your project
3. sets up **pre-commit** hooks — ruff, ruff-format, nbstripout
4. initialises a git repo with an initial commit

## comes with

**tools** — uv, ruff, pytest, pre-commit, nbstripout, jupyterlab, ipykernel

**geospatial stack** — xarray, rioxarray, rasterio, geopandas, pyproj

**storage** — zarr, netcdf4, h5netcdf, h5py, virtualizarr

**stac/odc** — pystac, pystac-client, odc-stac, odc-geo, odc-loader

**cloud** — boto3, s3fs, obstore

**compute** — dask, distributed, jax

**ml** — scikit-learn, mlflow

**viz** — matplotlib, cartopy, lonboard

## does not come with

places for your /data

## license

MIT