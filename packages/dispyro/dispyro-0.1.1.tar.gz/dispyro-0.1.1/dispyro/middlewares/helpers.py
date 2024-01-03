from dataclasses import dataclass
from typing import Any, Dict
from pyrogram import Client

from ..union_types import Update


@dataclass
class UpdateContext:
    client: Client
    update: Update
    data: Dict[str, Any]
