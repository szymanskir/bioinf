from .sequence import Sequence
from .sequence_alignment import SequenceAlignmentAlgorithmConfig
from configparser import ConfigParser


def read_sequence(filepath: str) -> Sequence:
    with open(filepath, "r") as f:
        raw_sequence = f.read()
    return Sequence(raw_sequence)


def read_config(filepath: str) -> SequenceAlignmentAlgorithmConfig:
    config: ConfigParser = ConfigParser()
    config.read(filepath)
    return SequenceAlignmentAlgorithmConfig(
        match=config["DEFAULT"].getint("match"),
        mismatch=config["DEFAULT"].getint("mismatch"),
        gap=config["DEFAULT"].getint("gap"),
        max_seq_len=config["DEFAULT"].getint("max_seq_len"),
        max_number_path=config["DEFAULT"].getint("max_number_path"),
    )
