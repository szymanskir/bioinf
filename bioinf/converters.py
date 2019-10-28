from .alignment import Alignment
from .path import Direction, Path
from .sequence import Sequence


class PathToAlignmentConverter:
    @staticmethod
    def convert(
        path: Path, left_sequence: Sequence, right_sequence: Sequence
    ) -> Alignment:
        left_sequence_alignment = ""
        right_sequence_alignment = ""
        left_index = len(left_sequence)
        right_index = len(right_sequence)

        for direction in path:
            if direction == Direction.DIAG:
                left_index = left_index - 1
                right_index = right_index - 1
                left_sequence_alignment = (
                    left_sequence[left_index] + left_sequence_alignment
                )
                right_sequence_alignment = (
                    right_sequence[right_index] + right_sequence_alignment
                )
            elif direction == Direction.UP:
                left_index = left_index - 1
                left_sequence_alignment = (
                    left_sequence[left_index] + left_sequence_alignment
                )
                right_sequence_alignment = "-" + right_sequence_alignment
            elif direction == Direction.LEFT:
                right_index = right_index - 1
                left_sequence_alignment = "-" + left_sequence_alignment
                right_sequence_alignment = (
                    right_sequence[right_index] + right_sequence_alignment
                )

        return Alignment(
            Sequence(left_sequence_alignment), Sequence(right_sequence_alignment)
        )
