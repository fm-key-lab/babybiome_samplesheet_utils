import sys

from importlib.metadata import PackageNotFoundError, version

from babybiome_samplesheet_utils import utils
from babybiome_samplesheet_utils.pathfinder import (
    PathFinder,
    FASTQPathFinder
)
from babybiome_samplesheet_utils.types import SamplesheetSchema


try:
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


def create_samplesheet(samples, directory):
    """Convenience function to create the sample sheet."""
    import pandas as pd

    fastq_finder = FASTQPathFinder(directory)
    fastq_paths = fastq_finder.find_paths(samples['ID'])

    return (
        pd.DataFrame.from_dict(fastq_paths, 'index')
        .rename_axis('ID')    
        .reset_index()
        .merge(samples, how='right')
        .explode(['fastq_1', 'fastq_2'])
    )


__all__ = [
    utils,
    PathFinder,
    FASTQPathFinder,
    SamplesheetSchema,
    create_samplesheet,
]