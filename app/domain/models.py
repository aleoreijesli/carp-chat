from typing import List
from pydantic import BaseModel


class Domain(BaseModel):
    id: str
    display_name: str
    keywords: List[str]
    aliases: List[str]
    threshold: int = 70   # fuzzy matching confidence
    active: bool = True
