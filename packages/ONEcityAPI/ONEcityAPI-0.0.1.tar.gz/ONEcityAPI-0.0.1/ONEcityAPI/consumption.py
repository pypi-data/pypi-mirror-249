from dataclasses import dataclass
from datetime import datetime


@dataclass
class Consumption:
    meterNumber: int
    externalWaterCardId: int
    siteExternalReferenceId: int
    readingTime: datetime
    totalWaterDataWithMultiplier: float
