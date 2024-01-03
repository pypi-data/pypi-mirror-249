#!/usr/bin/env python
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


class TestUtils:
    def test_promise_deprecation(self, recwarn):
        import TeleGenic.utils.promise  # noqa: F401

        assert len(recwarn) == 1
        assert str(recwarn[0].message) == (
            'TeleGenic.utils.promise is deprecated. Please use TeleGenic.ext.utils.promise instead.'
        )

    def test_webhookhandler_deprecation(self, recwarn):
        import TeleGenic.utils.webhookhandler  # noqa: F401

        assert len(recwarn) == 1
        assert str(recwarn[0].message) == (
            'TeleGenic.utils.webhookhandler is deprecated. Please use '
            'TeleGenic.ext.utils.webhookhandler instead.'
        )
