import logging


class Pipeline:
    def __init__(self, topic):
        self._topic = topic
        self.log = logging.getLogger("{}_pipeline".format(topic))

    def extract_source_image(self):
        self.log.info("Start to extract {} image...".format(self._topic))

    def train_image(self):
        self.log.info("Start to train {} image...".format(self._topic))

    def upload_trained_image(self):
        self.log.info("Start to upload {} image...".format(self._topic))
