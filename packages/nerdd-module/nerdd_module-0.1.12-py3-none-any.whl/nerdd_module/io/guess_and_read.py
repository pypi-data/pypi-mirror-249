import logging
from typing import Generator, List, Optional, Dict

from .elementary_reader import ElementaryReader
from .file_reader import FileReader
from .guessing_reader import GuessingReader
from .list_reader import ListReader
from .reader import MoleculeEntry, Reader
from .reader_registry import ReaderRegistry

__all__ = ["guess_and_read"]

logger = logging.getLogger(__name__)


def guess_and_read(
    input,
    input_format: Optional[str] = None,
    readers: Optional[List[Reader]] = None,
    num_test_entries: int = 10,
    hints: Dict = dict(),
) -> Generator[MoleculeEntry, None, None]:
    if readers is None:
        # filter readers by input_type (if specified)
        allowed_input_formats = ReaderRegistry().supported_input_formats
        if input_format is None:
            input_formats = allowed_input_formats
        else:
            assert input_format in allowed_input_formats
            input_formats = frozenset([input_format])

        # compose list of possible readers
        # the user is allowed to provide input as
        # 1. a string in one of the supported formats (e.g. "smiles")
        # 2. a list of strings that are *consistently* in of the supported formats 
        #    (e.g. [a smiles, another smiles, ...])
        # 3. a single file containing molecules in one of the supported formats
        # 4. a list of files (e.g. [a file, another file, ...]), but each file can
        #    be in a different format
            
        # 1.
        elementary_readers: List[Reader] = [
            reader
            for reader in ReaderRegistry()
            if reader.input_format in input_formats and isinstance(reader, ElementaryReader)
        ]

        # 2.
        list_readers: List[Reader] = [
            ListReader(inner_reader=reader) for reader in elementary_readers
        ]

        # 3.
        file_readers: List[Reader] = [
            reader
            for reader in ReaderRegistry()
            if reader.input_format in input_formats and isinstance(reader, FileReader)
        ]

        guessing_reader = GuessingReader(readers=file_readers, num_test_entries=num_test_entries)

        # 4.
        list_of_files_reader = ListReader(inner_reader=guessing_reader)

        # collect all readers
        readers = [
            *elementary_readers,
            *list_readers,
            list_of_files_reader,
            guessing_reader
        ]

    return GuessingReader(readers=readers, num_test_entries=num_test_entries).read(
        input
    )
