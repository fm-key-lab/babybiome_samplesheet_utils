from pathlib import Path

import pandas as pd
import pandera


class SamplesheetSchema(pandera.DataFrameModel):
    sample: int
    ID: str = pandera.Field(str_matches='^B00[12]-')
    fastq_1: str
    fastq_2: str
    
    @pandera.check('sample')
    def check_unique_sample_ids(cls, sample_ids):
        return sample_ids.size == sample_ids.nunique()

    @pandera.check('fastq_1')
    @pandera.check('fastq_2')
    def check_fastqs(cls, fastqs):
        return fastqs.apply(lambda x: pd.isna(x) or Path(x).is_file())