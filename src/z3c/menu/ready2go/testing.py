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
"""Testing Support
"""
import zope.security
from zope.container import contained
from zope.publisher.interfaces.browser import IBrowserView
from zope.site.testing import siteSetUp, siteTearDown

from z3c.menu.ready2go import interfaces, item


class TestParticipation(object):
    principal = 'foobar'
    interaction = None


class ISample(zope.interface.Interface):
    """Sample context interface."""


@zope.interface.implementer(ISample)
class Sample(object):
    """Sample context object."""

    def __init__(self, title):
        self.title = title


@zope.interface.implementer(IBrowserView)
class LocatableView(contained.Contained):

    def __init__(self, context, request):
        self.__parent__ = context
        self.context = context
        self.request = request

class IFirstView(IBrowserView):
    """First sample view interface."""

class ISecondView(IBrowserView):
    """Second sample view interface."""

@zope.interface.implementer(IFirstView)
class FirstView(LocatableView):
    """First view."""

@zope.interface.implementer(ISecondView)
class SecondView(LocatableView):
    """Second view."""


class IFirstMenu(interfaces.IMenuManager):
    """First menu manager."""

class ISecondMenu(interfaces.IMenuManager):
    """Second menu manager."""


class FirstMenuItem(item.ContextMenuItem):
    viewName = 'first.html'
    weight = 1

class SecondMenuItem(item.ContextMenuItem):
    viewName = 'second.html'
    weight = 2

def setUp(test):
    root = siteSetUp(True)
    test.globs['root'] = root

    from zope.traversing.testing import setUp
    setUp()

    from zope.browserpage import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)

    zope.security.management.newInteraction()
    zope.security.management.getInteraction().add(TestParticipation())


def tearDown(test):
    zope.security.management.endInteraction()
    siteTearDown()
