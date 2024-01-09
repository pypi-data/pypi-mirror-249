from abc import abstractmethod
from typing import BinaryIO, Generator

from .elementary_reader import ElementaryReader
from .reader import MoleculeEntry, Reader

__all__ = ["SplittingReader"]


class SplittingReader(Reader):

    def __init__(self, elementary_reader: ElementaryReader):
        super().__init__()
        self._elementary_reader = elementary_reader

    def read(self, input) -> Generator[MoleculeEntry, None, None]:
        if not hasattr(input, 'read'):
            raise TypeError("input must be a stream-like object")

        for block in self._split(input):
            yield from self._elementary_reader.read(block)

    @abstractmethod
    def _split(self, f: BinaryIO) -> Generator[str, None, None]:
        pass

    def _input_format(self) -> str:
        return self._elementary_reader.input_format
