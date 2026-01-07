from dataclasses import dataclass
@dataclass
class Track:
    id : int
    name : str
    album_id : int
    media_type_id : int
    genre_id : int
    composer: str
    milliseconds : int
    bytes : int
    unit_price : float


    def __str__(self):
        return f"{self.id} {self.name}"
    def __hash__(self):
        return hash(self.id)