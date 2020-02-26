from .base import BaseModel
from .message import sep_bytes
from ..api import UserApi
import random

API = UserApi.get_current


class Message(BaseModel):
    message_id: int = None
    flags: int = None
    peer_id: int = None
    timestamp: int = None
    text: str = None
    attachments: dict = None
    random_id: int = None

    async def get(self) -> dict:
        return (
            await API().request("messages.getById", {"message_ids": self.message_id})
        )["items"][0]

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2000000000

    @property
    async def from_id(self) -> int:
        return (await self.get())["from_id"]

    @property
    async def date(self) -> int:
        return (await self.get())["date"]

    @property
    async def out(self) -> int:
        return (await self.get())["out"]

    @property
    async def read_state(self) -> int:
        return (await self.get())["read_state"]

    async def reply(self, message: str = None, attachment: str = None, **params):

        locals().update(params)
        return await API().request(
            "messages.send",
            dict(
                peer_id=self.peer_id,
                reply_to=self.message_id,
                random_id=random.randint(-2e9, 2e9),
                **{
                    k: v
                    for k, v in locals().items()
                    if v is not None and k not in ["self", "params"]
                }
            ),
        )

    async def __call__(self, message: str = None, attachment: str = None, **params):

        locals().update(params)
        for message in sep_bytes(message or ""):
            m = await API().request(
                "messages.send",
                dict(
                    peer_id=self.peer_id,
                    random_id=random.randint(-2e9, 2e9),
                    **{
                        k: v
                        for k, v in locals().items()
                        if v is not None and k not in ["self", "params"]
                    }
                ),
            )
        return m
