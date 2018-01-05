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
import re
import unittest
import zope.interface
import zope.component
from zope.interface.verify import verifyClass, verifyObject
from zope.testing import renormalizing
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.component import hooks
from zope.site.testing import siteSetUp, siteTearDown

from z3c.menu.ready2go import interfaces, item, manager, testing

checker = renormalizing.RENormalizing([
    # Python 3 unicode removed the "u".
    (re.compile("u('.*?')"),
     r"\1"),
    (re.compile('u(".*?")'),
     r"\1"),
    ])


flags = doctest.NORMALIZE_WHITESPACE|\
        doctest.ELLIPSIS|\
        doctest.IGNORE_EXCEPTION_DETAIL

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


@zope.interface.implementer(IPhysicallyLocatable)
class ParentStub(object):
    """Just an object supporting a context attribtute."""

    __name__ = __parent__ = context = None

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
        zope.component.provideAdapter(CheckerStub, (None, None, None, None,
            None), interfaces.ISelectedChecker)
        super(GlobalMenuItemTest, self).setUp()

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
        zope.component.provideAdapter(CheckerStub, (None, None, None, None,
            None), interfaces.ISelectedChecker)

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
        zope.component.provideAdapter(CheckerStub, (None, None, None, None,
            None), interfaces.ISelectedChecker)

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
            optionflags=flags, checker=checker
            ),
        doctest.DocFileSuite('zcml.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=flags, checker=checker
            ),
        unittest.makeSuite(MenuManagerTest),
        unittest.makeSuite(GlobalMenuItemTest),
        unittest.makeSuite(SiteMenuItemTest),
        unittest.makeSuite(ContextMenuItemTest),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
