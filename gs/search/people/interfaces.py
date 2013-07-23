# coding=utf-8
from zope.interface import Interface
from zope.schema import TextLine

class IGSSearchPeople(Interface):
    email = TextLine(title=u'Email address',
      description=u'The email address of the person you wish to find.',
      required=True)

