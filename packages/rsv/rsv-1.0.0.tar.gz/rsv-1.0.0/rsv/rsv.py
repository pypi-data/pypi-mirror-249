from io import BytesIO
from typing import IO, Optional, List
from .encoder import Encoder
from .decoder import Decoder

# ! Encoding Methods
def dump(
    data: List[List[Optional[str]]],
    io: IO[bytes],
    encoding: str='utf-8',
    errors: str='strict'
) -> None:
    Encoder(io).dump(data, encoding, errors)

def dumps(
    data: List[List[Optional[str]]],
    encoding: str='utf-8',
    errors: str='strict'
) -> bytes:
    bio = BytesIO()
    Encoder(bio).dump(data, encoding, errors)
    bio.seek(0)
    return bio.read()

# ! Decoding Methods
def load(
    io: IO[bytes],
    encoding: str='utf-8',
    errors: str='strict'
) -> List[List[Optional[str]]]:
    return Decoder(io).load(encoding, errors)

def loads(
    data: bytes,
    encoding: str='utf-8',
    errors: str='strict'
) -> List[List[Optional[str]]]:
    return Decoder(BytesIO(data)).load(encoding, errors)