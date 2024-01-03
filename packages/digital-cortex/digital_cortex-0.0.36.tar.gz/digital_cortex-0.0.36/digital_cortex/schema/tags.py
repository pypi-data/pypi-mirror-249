from typing import List

from pydantic import BaseModel


class TagForm(BaseModel):
    id: str
    tagIds: List[str]
