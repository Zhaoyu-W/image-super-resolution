import json
import os
from datetime import datetime
import logging

import requests

from isr.utils.constants import ADOBE_URL, LIMIT
from isr.utils.blob_file_uploader import AzureBlobFileUploader

log = logging.getLogger(__name__)


class AdobeTask:
    def __init__(self, date_time=datetime.today(), limit=LIMIT):
        self.date_time = date_time
        self.limit = limit

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
        file_metadata = [{
            "title": file.get("title"),
            "adobe_id": file.get("id"),
            "img_url": file.get("thumbnail_url"),
        }
            for file in files
        ]
        azure_blob_file_uploader = AzureBlobFileUploader(
            "adobe", file_metadata=file_metadata, date_time=self.date_time)
        metadata = azure_blob_file_uploader.bulk_upload()

        return {"file_metadata": json.dumps(metadata)}

    def train_original_image(self, **context):
        log.info("Start to train adobe original images...")
        file_metadata = context["task_instance"].xcom_pull(task_ids="adobe_extract_task")["file_metadata"]
        print(json.loads(file_metadata))

        # TODO: fetch source image from blob, then train to sr image
        #try:
            # fd, path = tempfile.mkstemp()
            # with os.fdopen(fd, "wb") as tmp:
            #     tmp.write(img_data)
        # finally:
        #     os.remove(path)


    def upload_sr_image(self, **context):
        log.info("Start to upload adobe stock images...")
