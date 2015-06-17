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
from gs.group.member.base import user_member_of_group
from gs.profile.email.base import EmailUser
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

    @Lazy
    def groups(self):
        FOLDER_TYPES = ['Folder', 'Folder (ordered)']
        groups = getattr(self.context, 'groups')
        retval = [folder
                  for folder in groups.objectValues(FOLDER_TYPES)
                  if folder.getProperty('is_group', False)]
        return retval

    def email_info(self, userInfo):
        eu = EmailUser(self.context, userInfo)
        allEmail = eu.get_addresses()
        preferred = eu.get_delivery_addresses()
        unverified = eu.get_unverified_addresses()
        other = list(set(allEmail) - set(preferred) - set(unverified))
        retval = {'all': allEmail,
                  'preferred': preferred,
                  'other': other,
                  'unverified': unverified, }
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
                groups = [group.getId()
                          for group in self.groups
                          if user_member_of_group(userInfo, group)]
                r = {'id': userInfo.id,
                     'name': userInfo.name,
                     'url': ''.join((self.siteInfo.url, userInfo.url)),
                     'groups': groups,
                     'email': self.email_info(userInfo), }
        retval = to_json(r)
        return retval

    def handle_search_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        retval = self.build_error_response(action, data, errors)
        return retval
