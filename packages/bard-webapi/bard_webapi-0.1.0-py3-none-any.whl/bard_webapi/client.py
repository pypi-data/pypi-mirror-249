import re
import json
from typing import Optional

import httpx
from loguru import logger

from .const import HEADERS
from .utils import running
from .types import Chat, Image, Choice, ModelOutput


class BardClient:
    """
    Async httpx client interface for bard.google.com
    """

    def __init__(
        self,
        secure_1psid: str,
        secure_1psidts: Optional[str] = None,
        proxy: Optional[dict] = None,
    ):
        """
        Constructor.

        Parameters
        ----------
        secure_1psid: str
            __Secure-1PSID cookie value
        secure_1psidts: str, optional
            __Secure-1PSIDTS cookie value, some google accounts don't require this value, provide only if it's in the cookie list
        proxy: dict, optional
            dict of proxies
        """
        self.running = False
        self.posttoken = None
        self.client = httpx.AsyncClient(
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

    def newchat(self) -> Chat:
        """
        Create an empty chat object.

        Returns
        -------
        :class:`Chat`
            Empty chat object for retrieving conversation history
        """
        return Chat()

    @running
    async def generate(self, prompt: str, chat: Optional[Chat] = None) -> ModelOutput:
        """
        Generates contents with prompt.

        Parameters
        ----------
        prompt: str
            prompt provided by user
        chat: Chat, optional
            chat data to retrieve conversation history. If None, will automatically generate a new chat id when sending post request

        Returns
        -------
        :class:`ModelOutput`
            output data from bard.google.com, use `ModelOutput.text` to get the default text reply, `ModelOutput.images` to get a list
            of images in the default reply, `ModelOutput.choices` to get a list of all answer choices in the output
        """
        assert prompt, "Prompt cannot be empty."

        response = await self.client.post(
            "https://bard.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            data={
                "at": self.posttoken,
                "f.req": json.dumps(
                    [None, json.dumps([[prompt], None, chat and chat.list])]
                ),
            },
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to generate contents. Request failed with status code {response.status_code}"
            )
        else:
            body = json.loads(json.loads(response.text.split("\n")[2])[0][2])

            choices = []
            for choice in body[4]:
                images = (
                    choice[4]
                    and [Image(url=image[0][0][0], alt=image[2]) for image in choice[4]]
                    or []
                )
                choices.append(Choice(rcid=choice[0], text=choice[1][0], images=images))
            if not choices:
                raise Exception(
                    "Failed to generate contents. No output data found in response."
                )

            output = ModelOutput(chat=Chat(metadata=body[1]), choices=choices)
            if isinstance(chat, Chat):
                chat.metadata = output.chat.list  # update conversation history

            return output
