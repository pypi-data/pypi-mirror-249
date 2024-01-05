from dataclasses import dataclass


@dataclass
class Customer:
    number_of_persons: int
    rates: list
