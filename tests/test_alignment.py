from bioinf.alignment import Alignment
from bioinf.sequence import Sequence


def test_alignment_str():
    alignment: Alignment = Alignment(Sequence("ABC"), Sequence("BBC"))
    assert str(alignment) == "ABC\nBBC"
