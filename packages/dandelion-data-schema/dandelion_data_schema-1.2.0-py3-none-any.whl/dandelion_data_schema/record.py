
from typing import Dict, List, Optional, Union

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from .enum import SexEnum, RaceEnum, EthnicityEnum, ModalityType
from .lab import Lab, LabName
from .report import Report
from .study import ImagingStudy, WaveformStudy

class Record(BaseModel):
    model_config = ConfigDict(
        json_encoders = {
            np.ndarray: lambda v: v.tolist(),
        },
    )
    record_name: str
    age: Optional[float] = Field(..., ge=0, description='Age in years')
    sex: Optional[SexEnum]
    race: Optional[RaceEnum]
    ethnicity: Optional[EthnicityEnum]
    height: Optional[float] = Field(..., ge=0, description='Height in centimeters')
    weight: Optional[float] = Field(..., ge=0, description='Weight in kilograms')

    # diagnosis codes
    icd10: Optional[List[str]] = Field(None, alias='icd10')
    
    # modality data
    modality_type: ModalityType
    modality_data: Union[WaveformStudy, ImagingStudy]
    modality_report: Optional[Report] = Field(None, alias='report')

    # other modality information which may also be collected
    related_ecg: Optional[List[WaveformStudy]] = Field(None, alias='ecg')
    related_ct: Optional[List[ImagingStudy]] = Field(None, alias='ct')
    related_echo: Optional[List[ImagingStudy]] = Field(None, alias='echo')

    # lab data
    related_lab: Optional[Dict[LabName, Lab]] = Field(None, alias='lab')
