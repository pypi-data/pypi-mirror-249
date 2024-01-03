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
"""This module contains the :class:`TeleGenic.ext.utils.promise.Promise` class for backwards
compatibility.
"""
import warnings

import TeleGenic.ext.utils.promise as promise
from TeleGenic.utils.deprecate import TeleGenicDeprecationWarning

warnings.warn(
    'TeleGenic.utils.promise is deprecated. Please use TeleGenic.ext.utils.promise instead.',
    TeleGenicDeprecationWarning,
)

Promise = promise.Promise
"""
:class:`TeleGenic.ext.utils.promise.Promise`

.. deprecated:: v13.2
   Use :class:`TeleGenic.ext.utils.promise.Promise` instead.
"""
