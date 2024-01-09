from codecs import getreader
from typing import BinaryIO, Generator
from .reader import Reader
import gzip

from .file_reader import FileReader

__all__ = ["GzipFileReader"]

StreamReader = getreader("utf-8")


class GzipFileReader(FileReader):
    def __init__(self, inner_content_reader: Reader):
        super().__init__()
        self.inner_content_reader = inner_content_reader

    def _split(self, f: BinaryIO) -> Generator[str, None, None]:
        reader = StreamReader(f)
        for line in reader:
            # skip empty lines
            if line.strip() == "":
                continue

            # skip comments
            if line.strip().startswith("#"):
                continue

            yield line
