# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.form import SiteForm
from interfaces import IGSSearchPeople
from queries import SearchPeopleQuery

class SearchPeople(SiteForm):
    label = u'Search for People'
    pageTemplateFileName = 'browser/templates/searchpeople.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSSearchPeople, render_context=False)

    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)
    
    @Lazy
    def searchQuery(self):
        da = self.context.zsqlalchemy
        retval = SearchPeopleQuery(da)
        assert retval
        return retval
    
    @form.action(label=u'Search', failure='handle_search_action_failure')
    def handle_search(self, action, data):
    
        email = data['email']
        uids = self.searchQuery.find_uids_by_email(email)
    
        self.status = u'I should do stuff with %s.' % uids
        assert type(self.status) == unicode
        
    def handle_search_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode

