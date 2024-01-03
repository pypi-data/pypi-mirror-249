#!/usr/bin/env python
# pylint: disable=R0902,R0913
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
"""This module contains an object that represents a TeleGenic InlineQuery."""

from typing import TYPE_CHECKING, Any, Optional, Union, Callable, ClassVar, Sequence

from TeleGenic import Location, TeleGenicObject, User, constants
from TeleGenic.utils.helpers import DEFAULT_NONE
from TeleGenic.utils.types import JSONDict, ODVInput

if TYPE_CHECKING:
    from TeleGenic import Bot, InlineQueryResult


class InlineQuery(TeleGenicObject):
    """
    This object represents an incoming inline query. When the user sends an empty query, your bot
    could return some default or trending results.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`id` is equal.

    Note:
        In Python ``from`` is a reserved word, use ``from_user`` instead.

    Args:
        id (:obj:`str`): Unique identifier for this query.
        from_user (:class:`TeleGenic.User`): Sender.
        query (:obj:`str`): Text of the query (up to 256 characters).
        offset (:obj:`str`): Offset of the results to be returned, can be controlled by the bot.
        chat_type (:obj:`str`, optional): Type of the chat, from which the inline query was sent.
            Can be either :attr:`TeleGenic.Chat.SENDER` for a private chat with the inline query
            sender, :attr:`TeleGenic.Chat.PRIVATE`, :attr:`TeleGenic.Chat.GROUP`,
            :attr:`TeleGenic.Chat.SUPERGROUP` or :attr:`TeleGenic.Chat.CHANNEL`. The chat type should
            be always known for requests sent from official clients and most third-party clients,
            unless the request was sent from a secret chat.

            .. versionadded:: 13.5
        location (:class:`TeleGenic.Location`, optional): Sender location, only for bots that
            request user location.
        bot (:class:`TeleGenic.Bot`, optional): The Bot to use for instance methods.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.

    Attributes:
        id (:obj:`str`): Unique identifier for this query.
        from_user (:class:`TeleGenic.User`): Sender.
        query (:obj:`str`): Text of the query (up to 256 characters).
        offset (:obj:`str`): Offset of the results to be returned, can be controlled by the bot.
        location (:class:`TeleGenic.Location`): Optional. Sender location, only for bots that
            request user location.
        chat_type (:obj:`str`, optional): Type of the chat, from which the inline query was sent.

            .. versionadded:: 13.5

    """

    __slots__ = ('bot', 'location', 'chat_type', 'id', 'offset', 'from_user', 'query', '_id_attrs')

    def __init__(
        self,
        id: str,  # pylint: disable=W0622
        from_user: User,
        query: str,
        offset: str,
        location: Location = None,
        bot: 'Bot' = None,
        chat_type: str = None,
        **_kwargs: Any,
    ):
        # Required
        self.id = id  # pylint: disable=C0103
        self.from_user = from_user
        self.query = query
        self.offset = offset

        # Optional
        self.location = location
        self.chat_type = chat_type

        self.bot = bot
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: 'Bot') -> Optional['InlineQuery']:
        """See :meth:`TeleGenic.TeleGenicObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data['from_user'] = User.de_json(data.get('from'), bot)
        data['location'] = Location.de_json(data.get('location'), bot)

        return cls(bot=bot, **data)

    def answer(
        self,
        results: Union[
            Sequence['InlineQueryResult'], Callable[[int], Optional[Sequence['InlineQueryResult']]]
        ],
        cache_time: int = 300,
        is_personal: bool = None,
        next_offset: str = None,
        switch_pm_text: str = None,
        switch_pm_parameter: str = None,
        timeout: ODVInput[float] = DEFAULT_NONE,
        current_offset: str = None,
        api_kwargs: JSONDict = None,
        auto_pagination: bool = False,
    ) -> bool:
        """Shortcut for::

            bot.answer_inline_query(update.inline_query.id,
                                    *args,
                                    current_offset=self.offset if auto_pagination else None,
                                    **kwargs)

        For the documentation of the arguments, please see
        :meth:`TeleGenic.Bot.answer_inline_query`.

        Args:
            auto_pagination (:obj:`bool`, optional): If set to :obj:`True`, :attr:`offset` will be
                passed as :attr:`current_offset` to :meth:`TeleGenic.Bot.answer_inline_query`.
                Defaults to :obj:`False`.

        Raises:
            TypeError: If both :attr:`current_offset` and :attr:`auto_pagination` are supplied.
        """
        if current_offset and auto_pagination:
            # We raise TypeError instead of ValueError for backwards compatibility with versions
            # which didn't check this here but let Python do the checking
            raise TypeError('current_offset and auto_pagination are mutually exclusive!')
        return self.bot.answer_inline_query(
            inline_query_id=self.id,
            current_offset=self.offset if auto_pagination else current_offset,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
            timeout=timeout,
            api_kwargs=api_kwargs,
        )

    MAX_RESULTS: ClassVar[int] = constants.MAX_INLINE_QUERY_RESULTS
    """
    :const:`TeleGenic.constants.MAX_INLINE_QUERY_RESULTS`

    .. versionadded:: 13.2
    """
