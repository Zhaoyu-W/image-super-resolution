import json
import os
from datetime import datetime
import logging

import requests

from pipeline.utils.constants import ADOBE_URL, LIMIT
from pipeline.utils.blob_file_uploader import AzureBlobFileUploader
from pipeline.utils.cosmos_factory import CosmosFactory
from pipeline.utils.publish_util import publish_metadata

log = logging.getLogger(__name__)


class AdobeTask:
    SQL = "SELECT * FROM adobe a where a.id IN {}"

    def __init__(self, date_time=datetime.today(), limit=LIMIT):
        self.date_time = date_time
        self.limit = limit
        self.adobe_cosmos = CosmosFactory.get_container("adobe")

    def extract_source_image(self, **context):
        offset = self.date_time.hour*60 + self.date_time.minute
        log.info("[Adobe Extract (offset: {}, limit: {})] Start to extract adobe stock images...".format(
            offset, self.limit))

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-api-key": os.environ["ADOBE_API_KEY"],
            "x-product": os.environ["ADOBE_PRODUCT"],
        }

        files = requests.post(
            ADOBE_URL.format(self.limit, offset), headers=headers).json().get("files", [])
        file_ids = tuple([file.get("id") for file in files])
        trained_imgs = self.adobe_cosmos.query_items(
            self.SQL.format(str(file_ids)),
            enable_cross_partition_query=True
        )
        trained_ids = [
            img.get("id") for img in trained_imgs]
        log.info("Filter trained ids: {}".format(trained_ids))

        file_metadata = [{
            "title": file.get("title"),
            "adobe_id": file.get("id"),
            "img_url": file.get("thumbnail_url"),
        }
            for file in files
            if file.get("id") not in trained_ids
        ]
        azure_blob_file_uploader = AzureBlobFileUploader(
            "adobe", file_metadata=file_metadata, date_time=self.date_time)
        metadata = azure_blob_file_uploader.bulk_upload()

        return {"file_metadata": json.dumps(metadata)}

    def train_original_image(self, **context):
        log.info("Start to train adobe original images...")
        file_metadata = json.loads(
            context["task_instance"].xcom_pull(task_ids="adobe_extract_task")["file_metadata"])
        # TODO: fetch source image from blob, then train to sr image
        #try:
            # fd, path = tempfile.mkstemp()
            # with os.fdopen(fd, "wb") as tmp:
            #     tmp.write(img_data)
        # finally:
        #     os.remove(path)

        return {"trained_metadata": json.dumps(file_metadata)}

    def upload_sr_image(self, **context):
        log.info("Start to upload adobe stock images...")
        publish_metadata(json.loads(context["task_instance"].xcom_pull(
            task_ids="adobe_train_task")["trained_metadata"]), "adobe")
