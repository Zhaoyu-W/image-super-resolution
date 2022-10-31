import logging
import os
from datetime import datetime
from multiprocessing.pool import ThreadPool

import requests
from azure.storage.blob import BlobServiceClient, ContentSettings

# from isr.utils.constants import AZURE_CONF

log = logging.getLogger(__name__)


class AzureBlobFileUploader:
    def __init__(
            self,
            topic,
            file_metadata=None,
            date_time=datetime.today(),
            file_type="original",
            batch=10
    ):
        self.topic = topic
        self._connection_string = os.environ["AZURE_CONNECTION_STRING"]
        self._container_name = os.environ["{}_container_name".format(self.topic).upper()]
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self._connection_string)
        self.image_content_setting = ContentSettings(content_type="image/jpeg")
        self.file_metadata = file_metadata or []
        self.date_time = date_time
        self.file_type = file_type
        self.batch = batch

    def bulk_upload(self):
        result = self.run(self.file_metadata)
        return result

    def run(self, file_metadata):
        with ThreadPool(processes=self.batch) as pool:
            return pool.map(self.upload_image, file_metadata)

    def upload_image(self, metadata):
        raw_data = requests.get(metadata.get("img_url")).content
        file_name = metadata.get("title")
        file_path = "{}/{}/{}".format(
            self.date_time.strftime("%m-%d-%Y"), self.file_type, file_name)

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self._container_name, blob=file_path)
            blob_client.upload_blob(
                raw_data, overwrite=True, content_settings=self.image_content_setting)
            metadata["original_url"] = blob_client.url

            log.info("[Blob Uploader] Upload {} to Blob successfully!".format(
                self.topic, file_name))
            return metadata
        except Exception as e:
            log.error("[Blob Uploader]: Failed to upload {} due to {}".format(
                 file_name, e))
