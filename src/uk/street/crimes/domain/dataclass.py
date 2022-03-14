from dataclasses import dataclass
from typing import Optional


@dataclass
class StreetCrime:
    crime_id: str
    district_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    crime_type: Optional[str]
    last_outcome: Optional[str]


@dataclass
class StreetCrimeOutcome:
    crime_id: str
    outcome: str
