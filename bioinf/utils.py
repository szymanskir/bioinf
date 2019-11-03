from .sequence import Sequence
from .sequence_alignment import SequenceAlignmentAlgorithmConfig
from configparser import ConfigParser


class MissingConfigFieldError(Exception):
    """Class representing a missing config field error.
    """


class ImproperFastaFormatError(Exception):
    """Class representing an improper fasta format error.
    """


def read_sequence(filepath: str) -> Sequence:
    """Reads a protein sequence from the given file.

    Arguments:
        filepath {str} -- file in FASTA format from which the sequence should be read.

    Returns:
        (Sequence) -- sequence retrieved from the file.
    """
    with open(filepath, "r") as f:
        description = f.readline()
        if not description.startswith(">"):
            raise ImproperFastaFormatError(
                f"The description line of file {filepath} does not start with `>`"
            )
        raw_sequence = f.read().replace("\n", "")
    return Sequence(raw_sequence)


def read_config(filepath: str) -> SequenceAlignmentAlgorithmConfig:
    """Reads a config file from the given file.

    Arguments:
        filepath {str} -- file from which the config should be read.

    Raises:
        MissingConfigFieldError: if one of the required fields of
            SequenceAlignmentAlgorithmConfig is missing than an
            appropriate error is based.

    Returns:
        SequenceAlignmentAlgorithmConfig -- [description]
    """

    def assert_field(field, field_list):
        if field not in field_list:
            raise MissingConfigFieldError(
                f"The {field} field is missing from the config file."
            )

    required_fields = [
        "same",
        "diff",
        "gap_penalty",
        "max_seq_length",
        "max_number_paths",
    ]
    config: ConfigParser = ConfigParser()
    config.read(filepath)

    for field in required_fields:
        assert_field(field, dict(config["DEFAULT"]))

    return SequenceAlignmentAlgorithmConfig(
        same=config["DEFAULT"].getint("same"),
        diff=config["DEFAULT"].getint("diff"),
        gap_penalty=config["DEFAULT"].getint("gap_penalty"),
        max_seq_length=config["DEFAULT"].getint("max_seq_length"),
        max_number_paths=config["DEFAULT"].getint("max_number_paths"),
    )
