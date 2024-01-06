from typing import Any, Optional

from pydantic import BaseModel


class Chat(BaseModel):
    """
    Chat data to retrieve conversation history. Only if all 3 ids are provided will the conversation history be retrieved.

    Parameters
    ----------
    metadata: list[str], optional
        list of metadata [cid, rid, rcid], can be shorter than 3 elements, like [cid, rid] or [cid] only
    cid: str, optional
        chat id, if provided together with metadata, will override the first value in metadata
    rid: str, optional
        reply id, if provided together with metadata, will override the second value in metadata
    rcid: str, optional
        reply choice id, if provided together with metadata, will override the third value in metadata
    """
    metadata: Optional[list[str]] = None
    cid: Optional[str] = None  # chat id
    rid: Optional[str] = None  # reply id
    rcid: Optional[str] = None  # reply choice id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__metadata = [None, None, None]

        if self.metadata:
            if len(self.metadata) > 3:
                raise ValueError("metadata cannot exceed 3 elements")
            self.__metadata[: len(self.metadata)] = self.metadata
        if self.cid:
            self.__metadata[0] = self.cid
        if self.rid:
            self.__metadata[1] = self.rid
        if self.rcid:
            self.__metadata[2] = self.rcid

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "metadata":
            if len(value) > 3:
                raise ValueError("metadata cannot exceed 3 elements")
            self.__metadata[: len(value)] = value
        elif name == "cid":
            self.__metadata[0] = value
        elif name == "rid":
            self.__metadata[1] = value
        elif name == "rcid":
            self.__metadata[2] = value

        return super().__setattr__(name, value)

    @property
    def list(self):
        return self.__metadata


class Image(BaseModel):
    url: str
    alt: Optional[str] = "Image"

    def __str__(self):
        return f"[{self.alt}]({self.url})"


class Choice(BaseModel):
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
    chat: Chat
        chat data containing the most recent metadata
    choices: list[Choice]
        list of all choices returned from bard
    chosen: int, optional
        index of the chosen choice, by default will choose the first one
    """
    chat: Chat
    choices: list[Choice]
    chosen: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat.rcid = self.choices[self.chosen].rcid

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "chosen":
            self.chat.rcid = self.choices[value].rcid
        return super().__setattr__(name, value)

    def __str__(self):
        return self.text

    @property
    def text(self):
        return self.choices[self.chosen].text

    @property
    def images(self):
        return self.choices[self.chosen].images
