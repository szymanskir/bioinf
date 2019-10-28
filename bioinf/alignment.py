from dataclasses import dataclass


@dataclass
class Alignment:
    left_sequence_alignment: str
    right_sequence_alignment: str

    def __str__(self):
        return f"{self.left_sequence_alignment}\n{self.right_sequence_alignment}"
