# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, print_function, unicode_literals
from email.utils import parseaddr
from json import dumps as to_json
from logging import getLogger
log = getLogger('gs.search.profile.hook')
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.formlib import form
from gs.auth.token import log_auth_error
from gs.content.form.api.json import SiteEndpoint
from gs.profile.json import user_info, email_info, groups
from .interfaces import IUserExists
from .queries import SearchPeopleQuery


class ProfileExists(SiteEndpoint):
    '''The page determines if someone exits'''
    label = 'Profile exists'
    form_fields = form.Fields(IUserExists, render_context=False)

    @Lazy
    def query(self):
        retval = SearchPeopleQuery()
        return retval

    @form.action(label='Search', name='search', prefix='',
                 failure='handle_search_failure')
    def handle_search(self, action, data):
        '''The form action for the *simple* list

:param action: The button that was clicked.
:param dict data: The form data.'''
        if '@' in data['user']:  # It is an email address
            email = parseaddr(data['user'])[1]
            userId = self.query.find_uids_by_email(email)
        else:  # userId
            userId = data['user']
        r = {}
        if userId:
            userInfo = createObject('groupserver.UserFromId',
                                    self.context, userId)
            if not userInfo.anonymous:
                r = user_info(self.siteInfo, userInfo)
                r['groups'] = groups(self.siteInfo, userInfo)
                r['email'] = email_info(self.siteInfo, userInfo)
        retval = to_json(r)
        return retval

    def handle_search_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        retval = self.build_error_response(action, data, errors)
        return retval
