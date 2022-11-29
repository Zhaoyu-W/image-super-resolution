import json
import os
from datetime import datetime
import logging

import requests

from pipeline.utils.constants import PIXABAY_URL, LIMIT
from pipeline.utils.blob_file_uploader import AzureBlobFileUploader
from pipeline.utils.cosmos_factory import CosmosFactory
from pipeline.utils.publish_util import publish_metadata

log = logging.getLogger(__name__)


class PixabayTask:
    SQL = "SELECT * FROM pixabay p where p.id IN {}"

    def __init__(self, date_time=datetime.today(), limit=LIMIT):
        self.date_time = date_time
        self.limit = limit
        self.pixabay_cosmos = CosmosFactory.get_container("pixabay")

    def extract_source_image(self, **context):
        offset = self.date_time.hour*4 + self.date_time.minute/15
        log.info("[Pixabay Extract (offset: {}, limit: {})] Start to extract pixabay stock images...".format(
            offset, self.limit))

        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }

        files = requests.post(PIXABAY_URL.format(
            os.environ["PIXABAY_KEY"], self.limit, offset), headers=headers).json().get("hits", [])
        file_ids = tuple([file.get("id") for file in files])
        trained_imgs = self.pixabay_cosmos.query_items(
            self.SQL.format(str(file_ids)),
            enable_cross_partition_query=True
        )
        trained_ids = [
            img.get("id") for img in trained_imgs]
        log.info("Filter trained ids: {}".format(trained_ids))

        file_metadata = [{
            "title": file.get("tags"),
            "pixabay_id": file.get("id"),
            "img_url": file.get("webformatURL"),
        }
            for file in files
            if file.get("id") not in trained_ids
        ]

        azure_blob_file_uploader = AzureBlobFileUploader(
            "pixabay", file_metadata=file_metadata, date_time=self.date_time)
        metadata = azure_blob_file_uploader.bulk_upload()

        return {"file_metadata": json.dumps(metadata)}

    def train_original_image(self, **context):
        log.info("Start to train pixabay original images...")
        file_metadata = json.loads(
            context["task_instance"].xcom_pull(task_ids="pixabay_extract_task")["file_metadata"])
        # TODO: fetch source image from blob, then train to sr image
        #try:
            # fd, path = tempfile.mkstemp()
            # with os.fdopen(fd, "wb") as tmp:
            #     tmp.write(img_data)
        # finally:
        #     os.remove(path)

        return {"trained_metadata": json.dumps(file_metadata)}

    def upload_sr_image(self, **context):
        log.info("Start to upload pixabay stock images...")
        publish_metadata(json.loads(context["task_instance"].xcom_pull(
            task_ids="pixabay_train_task")["trained_metadata"]), "pixabay")
