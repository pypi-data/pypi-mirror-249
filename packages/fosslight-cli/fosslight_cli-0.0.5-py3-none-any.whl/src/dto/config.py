import dataclasses


@dataclasses.dataclass
class Config:
    server_url: str = None
    token: str = None
