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


class InputPaymentCredentialsApplePay(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputPaymentCredentials`.

    Details:
        - Layer: ``170``
        - ID: ``AA1C39F``

    Parameters:
        payment_data (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`):
            N/A

    """

    __slots__: List[str] = ["payment_data"]

    ID = 0xaa1c39f
    QUALNAME = "types.InputPaymentCredentialsApplePay"

    def __init__(self, *, payment_data: "raw.base.DataJSON") -> None:
        self.payment_data = payment_data  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPaymentCredentialsApplePay":
        # No flags
        
        payment_data = TLObject.read(b)
        
        return InputPaymentCredentialsApplePay(payment_data=payment_data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.payment_data.write())
        
        return b.getvalue()
