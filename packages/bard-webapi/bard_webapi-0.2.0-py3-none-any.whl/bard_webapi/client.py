import re
import json
from typing import Any, Optional

from httpx import AsyncClient
from loguru import logger

from .const import HEADERS
from .utils import running
from .types import Image, Candidate, ModelOutput


class BardClient:
    """
    Async httpx client interface for bard.google.com

    Parameters
    ----------
    secure_1psid: `str`
        __Secure-1PSID cookie value
    secure_1psidts: `str`, optional
        __Secure-1PSIDTS cookie value, some google accounts don't require this value, provide only if it's in the cookie list
    proxy: `dict`, optional
        Dict of proxies
    """

    __slots__ = ["running", "posttoken", "client"]

    def __init__(
        self,
        secure_1psid: str,
        secure_1psidts: Optional[str] = None,
        proxy: Optional[dict] = None,
    ):
        self.running: bool = False
        self.posttoken: Optional[str] = None
        self.client: AsyncClient = AsyncClient(
            timeout=20,
            proxies=proxy,
            follow_redirects=True,
            headers=HEADERS,
            cookies={
                "__Secure-1PSID": secure_1psid,
                "__Secure-1PSIDTS": secure_1psidts,
            },
        )

    async def init(self) -> None:
        """
        Get SNlM0e value as posting token. Without this token posting will fail with 400 bad request.
        """
        response = await self.client.get("https://bard.google.com/chat")

        if response.status_code != 200:
            await self.client.aclose()
            logger.error(
                f"Failed to initiate client. Request failed with status code {response.status_code}"
            )
        else:
            match = re.search(r'"SNlM0e":"(.*?)"', response.text)
            if match:
                self.posttoken = match.group(1)
                self.running = True
                logger.success("Bard client initiated successfully.")
            else:
                await self.client.aclose()
                logger.error(
                    "Failed to initiate client. SNlM0e not found in response, make sure cookie values are valid."
                )

    @running
    async def generate_content(
        self, prompt: str, chat: Optional["ChatSession"] = None
    ) -> ModelOutput:
        """
        Generates contents with prompt.

        Parameters
        ----------
        prompt: `str`
            Prompt provided by user
        chat: `ChatSession`, optional
            Chat data to retrieve conversation history. If None, will automatically generate a new chat id when sending post request

        Returns
        -------
        :class:`ModelOutput`
            Output data from bard.google.com, use `ModelOutput.text` to get the default text reply, `ModelOutput.images` to get a list
            of images in the default reply, `ModelOutput.candidates` to get a list of all answer candidates in the output
        """
        assert prompt, "Prompt cannot be empty."

        response = await self.client.post(
            "https://bard.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            data={
                "at": self.posttoken,
                "f.req": json.dumps(
                    [None, json.dumps([[prompt], None, chat and chat.metadata])]
                ),
            },
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to generate contents. Request failed with status code {response.status_code}"
            )
        else:
            body = json.loads(json.loads(response.text.split("\n")[2])[0][2])

            candidates = []
            for candidate in body[4]:
                images = (
                    candidate[4]
                    and [
                        Image(url=image[0][0][0], title=image[2], alt=image[0][4])
                        for image in candidate[4]
                    ]
                    or []
                )
                candidates.append(
                    Candidate(rcid=candidate[0], text=candidate[1][0], images=images)
                )
            if not candidates:
                raise Exception(
                    "Failed to generate contents. No output data found in response."
                )

            output = ModelOutput(metadata=body[1], candidates=candidates)

            if isinstance(chat, ChatSession):
                chat.output = output

            return output

    def start_chat(self, **kwargs) -> "ChatSession":
        """
        Returns a `ChatSession` object attached to this model.

        Returns
        -------
        :class:`ChatSession`
            Empty chat object for retrieving conversation history
        """
        return ChatSession(client=self, **kwargs)


class ChatSession:
    """
    Chat data to retrieve conversation history. Only if all 3 ids are provided will the conversation history be retrieved.

    Parameters
    ----------
    client: `BardClient`
        Async httpx client interface for bard.google.com
    metadata: `list[str]`, optional
        List of chat metadata `[cid, rid, rcid]`, can be shorter than 3 elements, like `[cid, rid]` or `[cid]` only
    cid: `str`, optional
        Chat id, if provided together with metadata, will override the first value in it
    rid: `str`, optional
        Reply id, if provided together with metadata, will override the second value in it
    rcid: `str`, optional
        Reply candidate id, if provided together with metadata, will override the third value in it
    """

    # @properties needn't have their slots pre-defined
    __slots__ = ["__metadata", "client", "output"]

    def __init__(
        self,
        client: BardClient,
        metadata: Optional[list[str]] = None,
        cid: Optional[str] = None,  # chat id
        rid: Optional[str] = None,  # reply id
        rcid: Optional[str] = None,  # reply candidate id
    ):
        self.__metadata: list[Optional[str]] = [None, None, None]
        self.client: BardClient = client
        self.output: Optional[ModelOutput] = None  # last output data

        if metadata:
            self.metadata = metadata
        if cid:
            self.cid = cid
        if rid:
            self.rid = rid
        if rcid:
            self.rcid = rcid

    def __str__(self):
        return f"ChatSession(cid={self.cid}, rid={self.rid}, rcid={self.rcid})"

    __repr__ = __str__

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        # update conversation history when last output is updated
        if name == "output" and isinstance(value, ModelOutput):
            self.metadata = value.metadata
            self.rcid = value.rcid

    async def send_message(self, prompt: str) -> ModelOutput:
        """
        Generates contents with prompt.
        Use as a shortcut for `BardClient.generate_content(prompt, self)`.

        Parameters
        ----------
        prompt: `str`
            Prompt provided by user

        Returns
        -------
        :class:`ModelOutput`
            Output data from bard.google.com, use `ModelOutput.text` to get the default text reply, `ModelOutput.images` to get a list
            of images in the default reply, `ModelOutput.candidates` to get a list of all answer candidates in the output
        """
        return await self.client.generate_content(prompt, self)

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, value: list[str]):
        if len(value) > 3:
            raise ValueError("metadata cannot exceed 3 elements")
        self.__metadata[: len(value)] = value

    @property
    def cid(self):
        return self.__metadata[0]

    @cid.setter
    def cid(self, value: str):
        self.__metadata[0] = value

    @property
    def rid(self):
        return self.__metadata[1]

    @rid.setter
    def rid(self, value: str):
        self.__metadata[1] = value

    @property
    def rcid(self):
        return self.__metadata[2]

    @rcid.setter
    def rcid(self, value: str):
        self.__metadata[2] = value
