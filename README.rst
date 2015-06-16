====================
``gs.search.people``
====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Search for GroupServer site members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-16
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This product provides the page_ that allows the site
administrator to search the members of a GroupServer_ site, and a
`web hook`_ to allow external systems to search for someone.

Page
====

The page ``admin_search_people.html``, in the context of the
site, allows the site administrator to search for a site
member.

:Note: The page is restricted to site members for privacy
       reasons.

Web hook
========

The web hook ``gs-search-people.json``, in the *site* context,
allows external systems to search for a person. It takes the
following parameters:

``token``:
  The authentication token [#token]_.

``email``:
  The email address to search.

``search``:
  The "form" action. (The value can be anything.)

:Note: Unlike the page_ the web hook searches **all people**,
       regardless of their site membership.

Return value
~~~~~~~~~~~~

If no profile was found then an empty JSON object is returned:
``{}``. Otherwise a JSON object is returned with the following
values.

``id``:
  The identifier of the profile.

``name``:
  The name of the person.

``url``:
  The URL of the profile.

``email``:
  The email addresses associated with the profile.

  * ``all``: All the addresses.
  * ``preferred``: The preferred address or addresses.
  * ``unverified``: The unverified addresses.
  * ``other``: The verified addresses that are not preferred.

Example
~~~~~~~

Calling with ``wget``:

.. code-block:: console

   $ wget --post-data='token=fake&email=a.person@home.example.com&search' \
     http://groups.example.com/gs-search-people.json

The returned JSON object:

.. code-block:: json

  {
    "id": "qK7SgjsTHcLNrJ2ClevcJ0",
    "name": "A. Person",
    "url": "https:/groups.example.com//p/qK7SgjsTHcLNrJ2ClevcJ0",
    "email": {
      "all": [
        "a.person@home.example.com",
        "a.person@work.example.com"
      ],
      "other": [
        "a.person@work.example.com"
      ],
      "preferred": [
        "a.person@home.example.com"
      ],
      "unverified": []
    }
  }

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.search.people
- Translations:
  https://www.transifex.com/projects/p/gs-search-people/
- Questions and comments to
  http://groupserver.org/groups/development/
- Report bugs at https://redmine.iopen.net/projects/groupserver/

.. [#token] See the ``gs.auth.token`` product for more
            information
            <https://github.com/groupserver/gs.auth.token>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
