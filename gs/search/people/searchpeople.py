# coding=utf-8
from email.utils import parseaddr
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.form import SiteForm
from gs.site.member import SiteMembers
from interfaces import IGSSearchPeople
from queries import SearchPeopleQuery


class SearchPeople(SiteForm):
    label = u'Search for a site member'
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
    
    @form.action(label=u'Search', failure='handle_search_action_failure')
    def handle_search(self, action, data):
    
        email = parseaddr(data['email'])[1]
        userId = self.searchQuery.find_uids_by_email(email)
        
        if userId and (userId in self.siteMembers):
            self.status = u'Be joyous! You found someone.'
            userInfo = createObject('groupserver.UserFromId',
                                    self.context, userId)
            uri = userInfo.url
            return self.request.RESPONSE.redirect(uri)
        else:
            self.status = u'Could not find any site-member with the '\
                u'email address <code class="email">%s</code>.' % email
        assert type(self.status) == unicode
        
    def handle_search_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode

