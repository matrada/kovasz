def test_geospatial_stack_imports():
    import geopandas
    import rasterio
    import rioxarray
    import xarray

    assert rasterio.__gdal_version__
    assert geopandas and rioxarray and xarray
