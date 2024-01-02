#!/usr/bin/env python
# pylint: disable=R0903
#
# A library that provides a Python interface to the TeleGenic Bot API
# Copyright (C) 2015-2022
# Leandro Toledo de Souza <devs@python-TeleGenic-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a TeleGenic Message Parse Modes."""
from typing import ClassVar

from TeleGenic import constants
from TeleGenic.utils.deprecate import set_new_attribute_deprecated


class ParseMode:
    """This object represents a TeleGenic Message Parse Modes."""

    __slots__ = ('__dict__',)

    MARKDOWN: ClassVar[str] = constants.PARSEMODE_MARKDOWN
    """:const:`TeleGenic.constants.PARSEMODE_MARKDOWN`\n

    Note:
        :attr:`MARKDOWN` is a legacy mode, retained by TeleGenic for backward compatibility.
        You should use :attr:`MARKDOWN_V2` instead.
    """
    MARKDOWN_V2: ClassVar[str] = constants.PARSEMODE_MARKDOWN_V2
    """:const:`TeleGenic.constants.PARSEMODE_MARKDOWN_V2`"""
    HTML: ClassVar[str] = constants.PARSEMODE_HTML
    """:const:`TeleGenic.constants.PARSEMODE_HTML`"""

    def __setattr__(self, key: str, value: object) -> None:
        set_new_attribute_deprecated(self, key, value)
