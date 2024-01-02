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


class SendCustomRequest(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``170``
        - ID: ``AA2769ED``

    Parameters:
        custom_method (``str``):
            N/A

        params (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`):
            N/A

    Returns:
        :obj:`DataJSON <pyrogram.raw.base.DataJSON>`
    """

    __slots__: List[str] = ["custom_method", "params"]

    ID = 0xaa2769ed
    QUALNAME = "functions.bots.SendCustomRequest"

    def __init__(self, *, custom_method: str, params: "raw.base.DataJSON") -> None:
        self.custom_method = custom_method  # string
        self.params = params  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendCustomRequest":
        # No flags
        
        custom_method = String.read(b)
        
        params = TLObject.read(b)
        
        return SendCustomRequest(custom_method=custom_method, params=params)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.custom_method))
        
        b.write(self.params.write())
        
        return b.getvalue()
