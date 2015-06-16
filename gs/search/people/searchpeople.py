# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014 OnlineGroups.net and Contributors.
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
from email.utils import parseaddr
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.base import SiteForm
from gs.site.member.base import SiteMembers
from .interfaces import IGSSearchPeople
from .queries import SearchPeopleQuery
from . import GSMessageFactory as _


class SearchPeople(SiteForm):
    label = _('search-people-form-label', 'Search for a site member')
    pageTemplateFileName = 'browser/templates/searchpeople.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSSearchPeople, render_context=False)

    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)
        self.searchQuery = SearchPeopleQuery()

    @Lazy
    def siteMembers(self):
        retval = SiteMembers(self.context)
        return retval

    @form.action(label=_('search-action', 'Search'),
                 failure='handle_search_action_failure')
    def handle_search(self, action, data):

        email = parseaddr(data['email'])[1]
        userId = self.searchQuery.find_uids_by_email(email)

        if userId and (userId in self.siteMembers):
            self.status = _('status-success',
                'Be joyous! You found someone.')
            userInfo = createObject('groupserver.UserFromId',
                                    self.context, userId)
            uri = userInfo.url
            return self.request.RESPONSE.redirect(uri)
        else:
            self.status = _('status-person-not-found',
                'Could not find any site-member with the email address '
                '<code class="email">${email}</code>.',
                mapping={'email': email})

    def handle_search_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = _('status-problem', '<p>There is an error:</p>')
        else:
            self.status = _('status-problems', '<p>There are errors:</p>')
