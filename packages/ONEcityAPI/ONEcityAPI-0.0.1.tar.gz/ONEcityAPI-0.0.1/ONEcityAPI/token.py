from dataclasses import dataclass


@dataclass
class Token:  # TODO implement token expiration
    token: str
    expires: int  # TODO check when token expires
