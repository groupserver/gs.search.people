# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from zope.interface import Interface
from zope.schema import TextLine


class IGSSearchPeople(Interface):
    email = TextLine(title='Email address',
                        description='The email address of the person you '
                                    'wish to find.',
                        required=True)
