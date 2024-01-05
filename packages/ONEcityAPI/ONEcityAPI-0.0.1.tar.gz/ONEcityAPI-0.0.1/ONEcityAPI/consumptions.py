from dataclasses import dataclass
from ONEcityAPI.consumption import Consumption


@dataclass
class Consumptions:
    consumption_list: list[Consumption]
