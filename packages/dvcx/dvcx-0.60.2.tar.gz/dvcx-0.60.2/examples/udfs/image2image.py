import json
import os

import fsspec
from PIL import Image, ImageFile, ImageFilter

from dql.catalog import get_catalog
from dql.query import C, DatasetQuery, DatasetRow, Object, udf
from dql.sql.types import Int32, String

cloud_prefix = "s3://"  # for GCP just switch to "gcs://"
bucket = "dql-50k-laion-files-writable"  # which bucket to use for both read and write
bucket_region = "us-east-2"  # no need to specify for GCP

file_type = "*.jpg"  # which files to use
blur_radius = 3  # how much to blur
filter_mod = 512  # how much of a subset of the data to use, i.e., 1/512

# only needed for AWS (no effect if using GCP)
os.environ["AWS_REGION"] = bucket_region
os.environ["AWS_DEFAULT_REGION"] = bucket_region

ImageFile.LOAD_TRUNCATED_IMAGES = True


def load_image(raw):
    img = Image.open(raw)
    img.load()
    return img


@udf(
    output={"anno": String, "width": Int32, "height": Int32},
    params=(
        Object(load_image),
        C.name,
    ),
)
class ImageFeatures:
    def __init__(self):
        pass

    def __call__(self, image, name):
        try:
            anno = {
                kk: vv
                for kk, vv in vars(image).items()
                if (not kk.startswith("_")) and isinstance(vv, (bool, int, float, str))
            }
            anno = json.dumps(anno)
            return (anno, image.width, image.height)
        except Exception as ex:
            print(f"ImageFeatures Error: {ex}")
            return (None,) * 3


@udf(
    output=DatasetRow.schema,
    params=(Object(load_image),) + tuple(DatasetRow.schema.keys()),
)
class Image2Image:
    def __init__(self, *, bucket_name, radius, prefix):
        self.folder_name = "blur"
        self.file_prefix = "blur_"
        self.prefix = prefix

        catalog = get_catalog()
        self.client, _ = catalog.parse_url(os.path.join(self.prefix, bucket_name))

        self.filter = ImageFilter.GaussianBlur(radius=radius)

    def save(self, image, source, name, format):
        # Make name for new image
        new_name = f"{self.file_prefix}{name}"

        # Do writeback
        blob_name = os.path.join(self.folder_name, new_name)
        urlpath = os.path.join(source, blob_name)
        cloud_file = fsspec.open(urlpath=urlpath, mode="wb")
        with cloud_file as fp:
            image.save(fp, format=format)

        # Get the blob info
        info_ = self.client.fs.info(urlpath)
        info = self.client._dict_from_info(info_, None, self.folder_name)
        info["name"] = new_name
        return info

    def __call__(
        self,
        image,
        *args,
    ):
        # Build a dict from row contents
        record = dict(zip(DatasetRow.schema.keys(), args))
        del record["random"]  # random will be populated automatically
        record["is_latest"] = record["is_latest"] > 0  # needs to be a bool

        # yield same row back
        yield DatasetRow.create(**record)

        # Don't apply the filter twice
        if record["parent"] == self.folder_name:
            return

        # Apply the filter
        image_b = image.filter(self.filter)

        # Save the image and get the cloud object info
        info = self.save(
            image_b, record["source"], name=record["name"], format=image.format
        )

        # Build the new row
        yield DatasetRow.create(
            name=info["name"],
            source=record["source"],
            parent=self.folder_name,
            size=info["size"],
            location=record["name"]
            if not record["parent"]
            else f"{record['parent']}/{record['name']}",
            vtype=record["vtype"],
            dir_type=record["dir_type"],
            owner_name=info["owner_name"],
            owner_id=info["owner_id"],
            is_latest=record["is_latest"],
            last_modified=info["last_modified"],
            version=info["version"],
            etag=info["etag"],
            anno=record["anno"],
        )


(
    DatasetQuery(os.path.join(cloud_prefix, bucket))
    .filter(C.name.glob(file_type))
    .filter(C.random % filter_mod == 0)
    .generate(Image2Image(bucket_name=bucket, radius=blur_radius, prefix=cloud_prefix))
    .add_signals(ImageFeatures)
)
