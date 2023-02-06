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
"""Test Setup
"""
import doctest
import unittest

import zope.component
import zope.interface
from zope.component import hooks
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from zope.site.testing import siteSetUp
from zope.site.testing import siteTearDown
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.interfaces import IPhysicallyLocatable

from z3c.menu.ready2go import interfaces
from z3c.menu.ready2go import item
from z3c.menu.ready2go import manager
from z3c.menu.ready2go import testing


flags = (
    doctest.NORMALIZE_WHITESPACE
    | doctest.ELLIPSIS
    | doctest.IGNORE_EXCEPTION_DETAIL
)


class CheckerStub:
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


@zope.interface.implementer(IPhysicallyLocatable)
class ParentStub:
    """Just an object supporting a context attribtute."""

    __name__ = __parent__ = context = None

    def __init__(self, path=('a', 'b')):
        self.path = path

    def getRoot(self):
        return self

    def getPath(self):
        return self.path


class AbsoulteURLStub:
    """Absolute url stub."""

    def __init__(self, context, request):
        pass

    def __str__(self):
        return 'here'

    __call__ = __str__


class InterfaceBaseTest(unittest.TestCase):
    """Base test for IContainer including interface test."""

    def makeTestObject(self):
        return self.getTestClass()(*self.getTestPos())

    def test_verifyClass(self):
        # class test
        self.assertTrue(
            verifyClass(self.getTestInterface(), self.getTestClass()))

    def test_verifyObject(self):
        # object test
        self.assertTrue(
            verifyObject(self.getTestInterface(), self.makeTestObject()))


class MenuManagerTest(InterfaceBaseTest):

    def getTestInterface(self):
        return interfaces.IMenuManager

    def getTestClass(self):
        return manager.MenuManager

    def getTestPos(self):
        return (None, None, None)


class GlobalMenuItemTest(InterfaceBaseTest):

    def setUp(self):
        site = siteSetUp(True)
        hooks.setSite(site)
        zope.component.provideAdapter(AbsoulteURLStub, (None, None),
                                      IAbsoluteURL)
        zope.component.provideAdapter(
            CheckerStub, (None, None, None, None, None),
            interfaces.ISelectedChecker)
        super().setUp()

    def tearDown(self):
        siteTearDown()

    def getTestInterface(self):
        return interfaces.IGlobalMenuItem

    def getTestClass(self):
        return item.GlobalMenuItem

    def getTestPos(self):
        return (ParentStub(), None, ParentStub(), None)


class SiteMenuItemTest(InterfaceBaseTest):

    def setUp(self):
        site = siteSetUp(True)
        hooks.setSite(site)
        zope.component.provideAdapter(AbsoulteURLStub, (None, None),
                                      IAbsoluteURL)
        zope.component.provideAdapter(
            CheckerStub, (None, None, None, None, None),
            interfaces.ISelectedChecker)

    def tearDown(self):
        siteTearDown()

    def getTestInterface(self):
        return interfaces.ISiteMenuItem

    def getTestClass(self):
        return item.SiteMenuItem

    def getTestPos(self):
        return (ParentStub(), None, ParentStub(), None)


class ContextMenuItemTest(InterfaceBaseTest):

    def setUp(self):
        zope.component.testing.setUp()
        zope.component.provideAdapter(AbsoulteURLStub, (None, None),
                                      IAbsoluteURL)
        zope.component.provideAdapter(
            CheckerStub, (None, None, None, None, None),
            interfaces.ISelectedChecker)

    def tearDown(self):
        zope.component.testing.tearDown()

    def getTestInterface(self):
        return interfaces.IContextMenuItem

    def getTestClass(self):
        return item.ContextMenuItem

    def getTestPos(self):
        return (None, None, ParentStub(), None)


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
                             setUp=testing.setUp, tearDown=testing.tearDown,
                             optionflags=flags,
                             ),
        doctest.DocFileSuite('zcml.txt',
                             setUp=testing.setUp, tearDown=testing.tearDown,
                             optionflags=flags,
                             ),
        unittest.defaultTestLoader.loadTestsFromTestCase(MenuManagerTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(GlobalMenuItemTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(SiteMenuItemTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(ContextMenuItemTest),
    ))
