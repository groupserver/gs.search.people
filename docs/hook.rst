========
Web hook
========

Synopsis
========

``/gs-search-people.json``? :option:`token` =<t> & :option:`user` =<u> & :option:`search`

Description
===========

The web hook ``gs-search-people.json``, in the *site* context,
allows external systems to search for a person.

Required arguments
==================

.. option:: token=<token>

  The authentication token [#token]_.

.. option:: user=<emailOrId>

  Either

  * An email address belonging to the person, or 
  * The user-identifier for the person.

.. option:: search

  The "form" action (no value needs to be set, but the argument
  must be present).

.. note:: Unlike the page (see :doc:`page`) the web hook searches
          **all people** that have a profile, regardless of their
          site membership. This can disclose a lot of
          information, so the data should be used cautiously.

Return value
============

If no profile was found then an empty JSON_ object is returned
(``{}``) . Otherwise a JSON object is returned with the standard
user-property values set (see `the core web-hook
documentation`_).

Example
=======

Using :program:`wget` to retrieve the profile information for
someone with the email address ``a.person@home.example.com`` from
the web-hook at ``groups.example.com``:

.. code-block:: console

   $ wget --post-data='token=fake&user=a.person@home.example.com&search' \
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
    "groups": [
      "example",
      "test"
    ],
  }

..  _JSON: http://json.org/

.. _the core web-hook documentation:
   http://groupserver.readthedocs.org/en/latest/webhook.html#profile-data

.. [#token] See ``gs.auth.token`` for more information
   <https://github.com/groupserver/gs.auth.token>

..  LocalWords:  JSON
