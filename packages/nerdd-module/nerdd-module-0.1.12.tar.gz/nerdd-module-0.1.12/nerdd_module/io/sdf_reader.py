from codecs import getreader
from typing import BinaryIO, Generator

from .elementary_mol_block_reader import ElementaryMolBlockReader
from .splitting_reader import SplittingReader

__all__ = ["SdfReader"]

StreamReader = getreader("utf-8")


class SdfReader(SplittingReader):
    def __init__(self, max_num_lines_mol_block: int = 10000):
        super().__init__(ElementaryMolBlockReader())
        self.max_num_lines_mol_block = max_num_lines_mol_block

    def _split(self, f: BinaryIO) -> Generator[str, None, None]:
        reader = StreamReader(f)

        while True:
            # collect lines to parse as a mol block
            mol_block = ""
            num_lines = 0
            line = reader.readline()
            while line:
                mol_block += line
                if line.strip() == "$$$$":
                    break

                num_lines += 1
                if num_lines > self.max_num_lines_mol_block:
                    break

                # read next line
                line = reader.readline()

            if mol_block.strip() != "":
                yield mol_block

            # We stop reading if
            # (1) we have reached the end of the file OR
            # (2) the last entry had more than MAX_NUM_LINES_MOL_BLOCK lines
            #     (this entry is probably not a valid mol block and everything after
            #      it is probably not a valid mol block either)
            if (not line) or (num_lines > self.max_num_lines_mol_block):
                break

    def __repr__(self) -> str:
        return f"SdfReader(max_num_lines_mol_block={self.max_num_lines_mol_block})"
