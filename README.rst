.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===========================
babybiome_samplesheet_utils
===========================


    Utils for "baby biome" sample info → tabular data


Utility functions to prepare sample info from the "baby biome" project as tabular data.

Usage
=====

.. code-block:: python

    import babybiome_samplesheet_utils as bbb
    import pandas as pd

    read_kwargs = {
        'engine': 'openpyxl',
        'names': ['ID', 'species']
    }

    samplesheet = (
        pd.read_excel('/path/to/samples.xlsx', **read_kwargs)
        .pipe(bbb.create_samplesheet, directory='/path/to/data')
        # Create unique `sample` identifier
        .rename_axis('sample')
        .reset_index()
        # NOTE: For real usage, log before blind drops
        .dropna()
        .pipe(bbb.SamplesheetSchema.validate)
    )

    # No paths were found for the following IDs:
    # B001-2406,
    # B001-2407,
    # B001-2408


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
