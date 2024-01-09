from codecs import getreader
from typing import BinaryIO, Generator

from .elementary_smiles_reader import ElementarySmilesReader
from .splitting_reader import SplittingReader

__all__ = ["SmilesReader"]


StreamReader = getreader("utf-8")


class SmilesReader(SplittingReader):
    def __init__(self):
        super().__init__(ElementarySmilesReader())

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
        return "SmilesReader()"