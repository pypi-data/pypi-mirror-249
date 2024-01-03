import os

from dql.lib.dataset import Dataset
from dql.lib.webdataset_meta import GenerateMeta, MergeParquetAndNpz
from dql.query.schema import C
from dql.sql.types import String

ds = Dataset("s3://dvcx-datacomp-small")
ds = ds.filter(C.name.glob("0020f*"))


# NOTE, this script does not work end-to-end due to a missing/not-optimized
# functionality such as binary column support and generator-based group-by.
# However, it's still useful to keep it in the codebase as a requirement.


def split_name(name):
    basename, ext = os.path.splitext(name)
    return (basename, ext.strip("."))


ds = ds.map(split_name, output={"basename": String, "ext": String})

# Lambda does work for single value output and produces 'result' column by default
# ds = ds.map(lambda name: os.path.splitext(name)[1].strip('.'))

ds = ds.aggregate(MergeParquetAndNpz(), partition_by=C.basename)
ds = ds.generate(GenerateMeta())

print(
    ds.limit(20)
    .select(C.parent, C.name, C.uid, C.clip_b32_similarity_score, C.b32_txt)
    .to_pandas()
)
