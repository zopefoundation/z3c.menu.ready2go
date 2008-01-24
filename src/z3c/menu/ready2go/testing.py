##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: tests.py 82943 2008-01-18 10:01:06Z rogerineichen $
"""
__docformat__ = 'restructuredtext'

import zope.security
from zope.publisher.interfaces.browser import IBrowserView
from zope.app.testing import setup
from zope.app.testing import ztapi
from zope.app.container import contained

from z3c.menu.ready2go import interfaces
from z3c.menu.ready2go import item


class TestParticipation(object):
    principal = 'foobar'
    interaction = None


class ISample(zope.interface.Interface):
    """Sample context interface."""


class Sample(object):
    """Sample context object."""

    zope.interface.implements(ISample)

    def __init__(self, title):
        self.title = title


class LocatableView(contained.Contained):

    zope.interface.implements(IBrowserView)

    def __init__(self, context, request):
        self.__parent__ = context
        self.context = context
        self.request = request

class IFirstView(IBrowserView):
    """First sample view interface."""

class ISecondView(IBrowserView):
    """Second sample view interface."""

class FirstView(LocatableView):
    """First view."""

    zope.interface.implements(IFirstView)

class SecondView(LocatableView):
    """Second view."""

    zope.interface.implements(ISecondView)


class IFirstMenu(interfaces.IMenuManager):
    """First menu manager."""

class ISecondMenu(interfaces.IMenuManager):
    """Second menu manager."""


class FirstMenuItem(item.ContextMenuItem):
    viewName = 'first.html'

class SecondMenuItem(item.ContextMenuItem):
    viewName = 'second.html'


def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root

    from zope.app.pagetemplate import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)

    zope.security.management.getInteraction().add(TestParticipation())


def tearDown(test):
    setup.placefulTearDown()
