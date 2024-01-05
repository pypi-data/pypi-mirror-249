"""test stuff."""

import os

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from hipscat.catalog.dataset.dataset import Dataset

import hipscat_import.index.run_index as runner
from hipscat_import.index.arguments import IndexArguments


def test_empty_args():
    """Runner should fail with empty arguments"""
    with pytest.raises(TypeError, match="IndexArguments"):
        runner.run(None)


def test_bad_args():
    """Runner should fail with mis-typed arguments"""
    args = {"output_artifact_name": "bad_arg_type"}
    with pytest.raises(TypeError, match="IndexArguments"):
        runner.run(args)


@pytest.mark.dask
def test_run_index(
    small_sky_object_catalog,
    tmp_path,
):
    """Test appropriate metadata is written"""

    args = IndexArguments(
        input_catalog_path=small_sky_object_catalog,
        indexing_column="id",
        output_path=tmp_path,
        output_artifact_name="small_sky_object_index",
        overwrite=True,
        progress_bar=False,
    )
    runner.run(args)

    # Check that the catalog metadata file exists
    catalog = Dataset.read_from_hipscat(args.catalog_path)
    assert catalog.on_disk
    assert catalog.catalog_path == args.catalog_path

    basic_index_parquet_schema = pa.schema(
        [
            pa.field("_hipscat_index", pa.uint64()),
            pa.field("Norder", pa.uint8()),
            pa.field("Dir", pa.uint64()),
            pa.field("Npix", pa.uint64()),
            pa.field("id", pa.int64()),
        ]
    )

    outfile = os.path.join(args.catalog_path, "index", "part.0.parquet")
    schema = pq.read_metadata(outfile).schema.to_arrow_schema()
    assert schema.equals(basic_index_parquet_schema, check_metadata=False)

    schema = pq.read_metadata(os.path.join(args.catalog_path, "_metadata")).schema.to_arrow_schema()
    assert schema.equals(basic_index_parquet_schema, check_metadata=False)

    schema = pq.read_metadata(os.path.join(args.catalog_path, "_common_metadata")).schema.to_arrow_schema()
    assert schema.equals(basic_index_parquet_schema, check_metadata=False)


@pytest.mark.dask
def test_run_index_on_source(
    small_sky_source_catalog,
    tmp_path,
):
    """Test appropriate metadata is written, when primary catalog covers multiple pixels."""

    args = IndexArguments(
        input_catalog_path=small_sky_source_catalog,
        indexing_column="source_id",
        output_path=tmp_path,
        output_artifact_name="small_sky_source_id_index",
        overwrite=True,
        progress_bar=False,
    )
    runner.run(args)

    # Check that the catalog metadata file exists
    catalog = Dataset.read_from_hipscat(args.catalog_path)
    assert catalog.on_disk
    assert catalog.catalog_path == args.catalog_path

    basic_index_parquet_schema = pa.schema(
        [
            pa.field("_hipscat_index", pa.uint64()),
            pa.field("Norder", pa.uint8()),
            pa.field("Dir", pa.uint64()),
            pa.field("Npix", pa.uint64()),
            pa.field("source_id", pa.int64()),
        ]
    )

    outfile = os.path.join(args.catalog_path, "index", "part.0.parquet")
    schema = pq.read_metadata(outfile).schema.to_arrow_schema()
    assert schema.equals(basic_index_parquet_schema, check_metadata=False)

    schema = pq.read_metadata(os.path.join(args.catalog_path, "_metadata")).schema.to_arrow_schema()
    assert schema.equals(basic_index_parquet_schema, check_metadata=False)

    schema = pq.read_metadata(os.path.join(args.catalog_path, "_common_metadata")).schema.to_arrow_schema()
    assert schema.equals(basic_index_parquet_schema, check_metadata=False)
