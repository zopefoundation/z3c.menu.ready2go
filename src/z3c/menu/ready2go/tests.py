##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
$Id: __init__.py 97 2007-03-29 22:58:27Z rineichen $
"""

import unittest
import zope.interface
import zope.component
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.app.component import hooks
from zope.app.testing import setup

import z3c.testing
from z3c.menu.ready2go import interfaces
from z3c.menu.ready2go import item
from z3c.menu.ready2go import manager
from z3c.menu.ready2go import testing


class CheckerStub(object):
    """Just a checker stub."""

    def __init__(self, context, request, view, menu, item):
        self.context = context
        self.request = request
        self.view = view
        self.menu = menu
        self.item = item

    @property
    def available(self):
        return True

    @property
    def selected(self):
        return True


class ParentStub(object):
    """Just an object supporting a context attribtute."""

    __name__ = __parent__ = context = None

    zope.interface.implements(IPhysicallyLocatable)

    def __init__(self, path=('a', 'b')):
        self.path = path

    def getRoot(self):
        return self

    def getPath(self):
        return self.path


class AbsoulteURLStub(object):
    """Absolute url stub."""

    def __init__(self, context, request):
        pass

    def __str__(self):
        return u'here'

    __call__ = __str__


class MenuManagerTest(z3c.testing.InterfaceBaseTest):

    def getTestInterface(self):
        return interfaces.IMenuManager

    def getTestClass(self):
        return manager.MenuManager

    def getTestPos(self):
        return (None, None, None)


class GlobalMenuItemTest(z3c.testing.InterfaceBaseTest):

    def setUp(self):
        site = setup.placefulSetUp(site=True)
        hooks.setSite(site)
        zope.component.provideAdapter(AbsoulteURLStub, (None, None),
            IAbsoluteURL)
        zope.component.provideAdapter(CheckerStub, (None, None, None, None,
            None), interfaces.ISelectedChecker)
        super(GlobalMenuItemTest, self).setUp()

    def getTestInterface(self):
        return interfaces.IGlobalMenuItem

    def getTestClass(self):
        return item.GlobalMenuItem

    def getTestPos(self):
        return (ParentStub(), None, ParentStub(), None)


class SiteMenuItemTest(z3c.testing.InterfaceBaseTest):

    def setUp(self):
        site = setup.placefulSetUp(site=True)
        hooks.setSite(site)
        zope.component.provideAdapter(AbsoulteURLStub, (None, None),
            IAbsoluteURL)
        zope.component.provideAdapter(CheckerStub, (None, None, None, None,
            None), interfaces.ISelectedChecker)
        super(SiteMenuItemTest, self).setUp()

    def getTestInterface(self):
        return interfaces.ISiteMenuItem

    def getTestClass(self):
        return item.SiteMenuItem

    def getTestPos(self):
        return (ParentStub(), None, ParentStub(), None)


class ContextMenuItemTest(z3c.testing.InterfaceBaseTest):

    def setUp(self):
        zope.component.provideAdapter(CheckerStub, (None, None, None, None,
            None), interfaces.ISelectedChecker)
        super(ContextMenuItemTest, self).setUp()

    def getTestInterface(self):
        return interfaces.IContextMenuItem

    def getTestClass(self):
        return item.ContextMenuItem

    def getTestPos(self):
        return (None, None, ParentStub(), None)


def test_suite():
    return unittest.TestSuite((
        DocFileSuite('README.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        DocFileSuite('zcml.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        unittest.makeSuite(MenuManagerTest),
        unittest.makeSuite(GlobalMenuItemTest),
        unittest.makeSuite(SiteMenuItemTest),
        unittest.makeSuite(ContextMenuItemTest),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
