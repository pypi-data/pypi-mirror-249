from dql.lib.dataset import Dataset
from dql.lib.webdataset import WebDataset
from dql.query.schema import C
from dql.sql.types import Int, String

ds = Dataset("s3://dvcx-datacomp-small").filter(C.name.glob("00000001.tar"))

wds = ds.generate(
    WebDataset(
        json_to_flatten={
            "uid": String,
            "width": Int,
            "height": Int,
            "sha256": String,
        },
        extensions=["json", "index", "cls2"],
    ),
    parallel=-1,
)

print(wds.select(C.parent, C.name, C.uid, C.width, C.height).to_pandas())
