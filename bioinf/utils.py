from .sequence import SequenceAlignmentAlgorithmConfig
from configparser import ConfigParser


def read_sequence(filepath: str) -> str:
    with open(filepath, "r") as f:
        sequence = f.read()
    return sequence


def read_config(filepath: str) -> SequenceAlignmentAlgorithmConfig:
    config: ConfigParser = ConfigParser()
    config.read(filepath)
    return SequenceAlignmentAlgorithmConfig(
        config["DEFAULT"].getint("match"),
        config["DEFAULT"].getint("mismatch"),
        config["DEFAULT"].getint("gap"),
    )
