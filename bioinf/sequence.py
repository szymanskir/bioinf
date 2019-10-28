class Sequence:
    """Class representing a protein sequence.

    Attributes:
        _raw_sequence (str): Raw string representation of the protein sequence.
    """

    def __init__(self, raw_sequence: str):
        self._raw_sequence: str = raw_sequence

    def __getitem__(self, index: int):
        return self._raw_sequence[index]

    def __iter__(self):
        return iter(self._raw_sequence)

    def __len__(self) -> int:
        return len(self._raw_sequence)

    def __str__(self):
        return self._raw_sequence
