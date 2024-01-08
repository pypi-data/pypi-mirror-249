# mp4_utils/core/mp4_handler.py
from base_model.MediaHandler import MediaHandler


class MP4Handler(MediaHandler):
    """
    Class for handling MP4 files.
    """

    def __init__(self, file_path):
        super().__init__(file_path)

    def process(self, *args, **kwargs):
        # Implementation specific to MP4 processing
        pass
