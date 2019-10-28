from dataclasses import dataclass
from .sequence import Sequence


@dataclass
class Alignment:
    left_sequence_alignment: Sequence
    right_sequence_alignment: Sequence

    def __str__(self):
        return f"{self.left_sequence_alignment}\n{self.right_sequence_alignment}"
