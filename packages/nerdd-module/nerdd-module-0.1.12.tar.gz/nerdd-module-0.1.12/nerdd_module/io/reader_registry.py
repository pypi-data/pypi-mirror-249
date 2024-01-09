from functools import lru_cache

from .inchi_reader import InchiReader
from .elementary_inchi_reader import ElementaryInchiReader
from .elementary_mol_block_reader import ElementaryMolBlockReader
from .elementary_rdkit_mol_reader import ElementaryRdkitMolReader
from .reader import Reader
from .sdf_reader import SdfReader
from .smiles_reader import SmilesReader
from .elementary_smiles_reader import ElementarySmilesReader
from .file_reader import FileReader

__all__ = ["ReaderRegistry"]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class ReaderRegistry:
    def __init__(self):
        self._readers = []

    def register(self, reader: Reader):
        self._readers.append(reader)

    @property
    def supported_input_formats(self) -> frozenset:
        return frozenset([reader.input_format for reader in self._readers])

    @property
    def readers(self):
        return frozenset(self._readers)

    def __iter__(self):
        return iter(self._readers)


registry = ReaderRegistry()
registry.register(ElementarySmilesReader())
registry.register(ElementaryInchiReader())
registry.register(ElementaryMolBlockReader())
registry.register(ElementaryRdkitMolReader())
registry.register(FileReader(SdfReader(max_num_lines_mol_block=10_000)))
registry.register(FileReader(SmilesReader()))
registry.register(FileReader(InchiReader()))
