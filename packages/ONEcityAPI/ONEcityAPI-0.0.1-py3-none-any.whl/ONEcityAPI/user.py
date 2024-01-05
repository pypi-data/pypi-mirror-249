from dataclasses import dataclass


@dataclass
class User:
    userName: str
    password: str
    customerID: str
    customerSite: str
