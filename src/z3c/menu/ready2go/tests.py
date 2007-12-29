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
import zope.component
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.app.component import hooks
from zope.app.testing import setup

import z3c.testing
from z3c.menu.ready2go import interfaces
from z3c.menu.ready2go import item
from z3c.menu.ready2go import manager


class ParentStub(object):
    """Just an object supporting a context attribtute."""

    context = None
    __name__ = None


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
        super(GlobalMenuItemTest, self).setUp()

    def getTestInterface(self):
        return interfaces.IGlobalMenuItem

    def getTestClass(self):
        return item.GlobalMenuItem

    def getTestPos(self):
        return (None, None, ParentStub(), None)


class ContextMenuItemTest(z3c.testing.InterfaceBaseTest):

    def getTestInterface(self):
        return interfaces.IContextMenuItem

    def getTestClass(self):
        return item.ContextMenuItem

    def getTestPos(self):
        return (None, None, ParentStub(), None)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(MenuManagerTest),
        unittest.makeSuite(GlobalMenuItemTest),
        unittest.makeSuite(ContextMenuItemTest),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
