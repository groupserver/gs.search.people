# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.search.people',
    version=version,
    description="Searching for people on GroupServer.",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='site groupserver name',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='http://groupserver.org/',
    license='other',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.search', ],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
        'sqlalchemy',
        'Zope2',
        'zope.cachedescriptors',
        'zope.component',
        'zope.formlib',
        'zope.interface',
        'zope.schema',
        'gs.content.form',
        'gs.database',
        'gs.site.member',
        'Products.GSContent',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
