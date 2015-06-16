# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.interface import Interface
from zope.schema import TextLine, ASCIILine
from gs.auth.token import AuthToken
from . import GSMessageFactory as _


class IGSSearchPeople(Interface):
    email = TextLine(
        title=_('email-entry-label', 'Email address'),
        description=_(
            'email-entry-description',
            'The email address of the person you wish to find.'),
        required=True)


class IUserExists(Interface):
    'Determine if a user exists'

    email = ASCIILine(
        title='Email address',
        description='The person that is being searched',
        required=True)

    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)
