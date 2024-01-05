from enum import Enum

class ModalityType(str, Enum):
    waveform = "waveform"
    dicom = "dicom"

class SexEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class RaceEnum(str, Enum):
    white = "White"
    black = "Black or African American"
    asian = "Asian American or Pacific Islander"
    native = "American Indian or Native Alaskan"

class EthnicityEnum(str, Enum):
    hispanic = "Hispanic"
    non_hispanic = "Non-Hispanic"

class ModelOutputType(str, Enum):
    """The type of problem the model is designed to solve."""
    binary = "binary"
    multiclass = "multiclass"
    multilabel = "multilabel"
    regression = "regression"
