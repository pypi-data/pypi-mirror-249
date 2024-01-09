from codecs import getreader
from typing import BinaryIO, Generator

from .elementary_inchi_reader import ElementaryInchiReader
from .splitting_reader import SplittingReader

__all__ = ["InchiReader"]

StreamReader = getreader("utf-8")


class InchiReader(SplittingReader):
    def __init__(self):
        super().__init__(ElementaryInchiReader())

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

    def __repr__(self) -> str:
        return "InchiReader()"