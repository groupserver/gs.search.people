# coding=utf-8
import sqlalchemy as sa

class SearchPeopleQuery(object):
    def __init__(self, da):
        self.userEmailTable = da.createTable('user_email')

    def find_uids_by_email(self, emailAddress):
        uet = self.userEmailTable
        s = sa.select([uet.c.user_id])
        expr = '%%%s%%' % emailAddress
        s.append_whereclause(uet.c.email.op('ILIKE')(expr))
    
        r = s.execute()
        retval = [x['user_id'] for x in r]
        assert type(retval) == list
        return retval

