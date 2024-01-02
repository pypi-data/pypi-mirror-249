#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class GetBotApp(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``170``
        - ID: ``34FDC5C3``

    Parameters:
        app (:obj:`InputBotApp <pyrogram.raw.base.InputBotApp>`):
            N/A

        hash (``int`` ``64-bit``):
            N/A

    Returns:
        :obj:`messages.BotApp <pyrogram.raw.base.messages.BotApp>`
    """

    __slots__: List[str] = ["app", "hash"]

    ID = 0x34fdc5c3
    QUALNAME = "functions.messages.GetBotApp"

    def __init__(self, *, app: "raw.base.InputBotApp", hash: int) -> None:
        self.app = app  # InputBotApp
        self.hash = hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBotApp":
        # No flags
        
        app = TLObject.read(b)
        
        hash = Long.read(b)
        
        return GetBotApp(app=app, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.app.write())
        
        b.write(Long(self.hash))
        
        return b.getvalue()
