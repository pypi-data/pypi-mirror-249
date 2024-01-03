from dql.lib.udf import Aggregator, Generator
from dql.query import DatasetRow, LocalFilename
from dql.sql.types import Array, Binary, Float32, Int64, String

try:
    import pandas as pd
except ImportError:
    pd = None


def union_dicts(*dicts):
    """Union dictionaries.
    Equivalent to `d1 | d2 | d3` in Python3.9+ but works in older versions.
    """
    result = None
    for d in dicts:
        if not isinstance(d, dict):
            raise ValueError("All arguments must be dictionaries.")
        if not result:
            result = d.copy()
        else:
            result.update(d)
    return result


# We need to merge parquet and npz data first because they need to be
# used together for generating multiple records.
# It won't be a requirement when aggregator will generator based.
class MergeParquetAndNpz(Aggregator):
    def __init__(self):
        super().__init__(
            (
                "ext",
                LocalFilename(),
            ),
            {"parquet_data": Binary, "npz_data": Binary},
        )

    def process(self, args):
        group_params_fname = ["ext", "fname"]
        df = pd.DataFrame(args, columns=group_params_fname)

        fname_npz = df[df.ext == "npz"].fname.iloc[0]
        fname_pq = df[df.ext == "parquet"].fname.iloc[0]
        npz_data = open(fname_npz, "rb").read(1024 * 1024)  # HACK
        pq_data = open(fname_pq, "rb").read()

        df["npz_data"] = df.ext.apply(lambda x: npz_data if x == "parquet" else None)
        df["parquet_data"] = df.ext.apply(lambda x: pq_data if x == "parquet" else None)

        df = df.drop(["ext", "fname"], axis=1)
        return tuple(map(tuple, df.values))


class GenerateMeta(Generator):
    PQ_SCHEMA = {
        "uid": String,
        "url": String,
        "text": String,
        "original_width": Int64,
        "original_height": Int64,
        "clip_b32_similarity_score": Float32,
        "clip_l14_similarity_score": Float32,
        "face_bboxes": Array(Array(Float32)),
        "sha256": String,
    }

    NPZ_SCHEMA = {
        "b32_img": Array(Float32),
        "b32_txt": Array(Float32),
        "l14_img": Array(Float32),
        "l14_txt": Array(Float32),
        "dedup": Array(Float32),
    }

    META_SCHEMA = {**PQ_SCHEMA, **NPZ_SCHEMA}

    def __init__(self):
        super().__init__(
            ("source", "parent", "name", "etag", "parquet_data", "npz_data"),
            self.META_SCHEMA,
        )

    def process(self, source, parent, name, etag, parquet_data, npz_data):
        if parquet_data is None or npz_data is None:
            return DatasetRow.create(name, source=source, parent=parent, etag=etag) + (
                None,
            ) * len(self.META_SCHEMA)

        # Hack until bin data issues is solved
        pq_fname = f"{parent}/{name}"
        # npz_fname = os.path.splitext(pq_fname)[0] + ".npz"

        df = pd.read_parquet(pq_fname)
        df = df.head(1000)
        # npz = np.load(npz_fname)

        for idx, (_, row) in enumerate(df.iterrows()):
            row_basic = DatasetRow.create(
                str(idx),
                source=source,
                parent=f"{parent}/{name}",
                etag=etag,
                vtype="parquet",
            )

            pq_payload = tuple([row[key] for key in self.PQ_SCHEMA.keys()])
            # npz_payload = tuple([npz[key][idx] for key in self.NPZ_SCHEMA.keys()])
            npz_payload = tuple([None] * len(self.NPZ_SCHEMA))

            yield row_basic + pq_payload + npz_payload
