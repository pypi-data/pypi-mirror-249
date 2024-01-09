from typing import Iterable, Optional, Tuple

from rdkit.Chem import Mol

from .elementary_reader import ElementaryReader

__all__ = ["ElementaryRdkitMolReader"]


class ElementaryRdkitMolReader(ElementaryReader):
    def __init__(self):
        super().__init__()

    def _read(self, input) -> Tuple[Optional[Mol], Iterable[str]]:
        if not isinstance(input, Mol):
            raise TypeError("input must be a mol")

        return input, []

    def _input_format(self) -> str:
        return "rdkit_mol"

    def __repr__(self) -> str:
        return "ElementaryRdkitMolReader()"