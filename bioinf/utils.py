from .sequence import Sequence
from .sequence_alignment import SequenceAlignmentAlgorithmConfig
from configparser import ConfigParser
from typing import List


class MissingConfigFieldError(Exception):
    """Class representing a missing config field error.
    """


def read_sequence(filepath: str) -> Sequence:
    """Reads a protein sequence from the given file.
    
    Arguments:
        filepath {str} -- file from which the sequence should be read.
    
    Returns:
        (Sequence) -- sequence retrieved from the file.
    """
    with open(filepath, "r") as f:
        raw_sequence = f.read()
    return Sequence(raw_sequence)


def read_config(filepath: str) -> SequenceAlignmentAlgorithmConfig:
    """Reads a config file from the given file.
    
    Arguments:
        filepath {str} -- file from which the config should be read.
    
    Raises:
        MissingConfigFieldError: if one of the required fields of
            SequenceAlignmentAlgorithmConfig is missing than an appropriate error is based.
    
    Returns:
        SequenceAlignmentAlgorithmConfig -- [description]
    """

    def assert_field(field, field_list):
        if field not in field_list:
            raise MissingConfigFieldError(
                f"The {field} field is missing from the config file."
            )

    required_fields = ["match", "mismatch", "gap", "max_seq_len", "max_number_path"]
    config: ConfigParser = ConfigParser()
    config.read(filepath)

    for field in required_fields:
        assert_field(field, dict(config["DEFAULT"]))

    return SequenceAlignmentAlgorithmConfig(
        match=config["DEFAULT"].getint("match"),
        mismatch=config["DEFAULT"].getint("mismatch"),
        gap=config["DEFAULT"].getint("gap"),
        max_seq_len=config["DEFAULT"].getint("max_seq_len"),
        max_number_path=config["DEFAULT"].getint("max_number_path"),
    )
