# -*- coding: utf-8 -*-
import sqlalchemy as sa
from gs.database import getTable, getSession


class SearchPeopleQuery(object):
    def __init__(self):
        self.userEmailTable = getTable('user_email')

    def find_uids_by_email(self, emailAddress):
        uet = self.userEmailTable
        s = sa.select([uet.c.user_id])
        # Use an ILIKE so the search is case insensitive.
        expr = '%s' % emailAddress
        s.append_whereclause(uet.c.email.op('ILIKE')(expr))

        session = getSession()
        r = session.execute(s)
        rv = [x['user_id'] for x in r]
        retval = (rv and rv[0]) or None
        return retval
