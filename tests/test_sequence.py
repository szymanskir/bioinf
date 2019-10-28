from bioinf.sequence import Sequence


def test_sequence_str():
    sequence: Sequence = Sequence("ABC")
    assert str(sequence) == "ABC"
