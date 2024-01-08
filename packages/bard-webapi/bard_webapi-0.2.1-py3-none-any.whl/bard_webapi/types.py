from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    title: Optional[str] = "[Image]"
    alt: Optional[str] = ""

    def __str__(self):
        return f"{self.title}({self.url}) - {self.alt}"


class Candidate(BaseModel):
    rcid: str
    text: str
    images: list[Image]

    def __str__(self):
        return self.text


class ModelOutput(BaseModel):
    """
    Classified output from bard.google.com

    Parameters
    ----------
    metadata: `list[str]`
        List of chat metadata `[cid, rid, rcid]`, can be shorter than 3 elements, like `[cid, rid]` or `[cid]` only
    candidates: `list[Candidate]`
        List of all candidates returned from bard
    chosen: `int`, optional
        Index of the chosen candidate, by default will choose the first one
    """

    metadata: list[str]
    candidates: list[Candidate]
    chosen: int = 0

    def __str__(self):
        return self.text

    @property
    def text(self):
        return self.candidates[self.chosen].text

    @property
    def images(self):
        return self.candidates[self.chosen].images

    @property
    def rcid(self):
        return self.candidates[self.chosen].rcid
