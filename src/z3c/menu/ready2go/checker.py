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
"""Menu Item "Selected Checker"
"""
import zope.interface
import zope.component
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.menu.ready2go import interfaces


class CheckerBase(object):
    """Generic checker base class."""

    def __init__(self, context, request, view, menu, item):
        self.context = context
        self.request = request
        self.view = view
        self.menu = menu
        self.item = item


# ISelectedChecker
@zope.interface.implementer(interfaces.ISelectedChecker)
class FalseSelectedChecker(CheckerBase):
    """False selected checker can avoid selected menu item rendering."""

    @property
    def selected(self):
        return False


@zope.interface.implementer(interfaces.ISelectedChecker)
class TrueSelectedChecker(CheckerBase):
    """True selected checker can force selected menu item rendering."""

    @property
    def selected(self):
        return True


@zope.interface.implementer(interfaces.ISelectedChecker)
class ViewNameSelectedChecker(CheckerBase):
    """Selected by view name offers a generic checker for IContextMenuItem."""

    @property
    def selected(self):
        """Selected if also view name compares."""
        viewName = self.item.viewName
        if viewName.startswith('@@'):
            viewName = viewName[2:]
        if self.view.__name__ == viewName:
            return True
        return False


# default selected checkers
class GlobalSelectedChecker(FalseSelectedChecker):
    """Global menu item selected checker.
    
    Note, this is a menu group which is selected on different menu items.
    You need to register for each view a TrueSelectedChecker if the site menu
    item should get rendered as selected.
    """

    zope.component.adapts(zope.interface.Interface, IBrowserRequest,
        zope.interface.Interface, interfaces.IMenuManager,
        interfaces.IGlobalMenuItem)


class SiteSelectedChecker(FalseSelectedChecker):
    """Site menu item selected checker.
    
    Note, this is a menu group which is selected on different menu items.
    You need to register for each view a TrueSelectedChecker if the site menu
    item should get rendered as selected.
    """

    zope.component.adapts(zope.interface.Interface, IBrowserRequest,
        zope.interface.Interface, interfaces.IMenuManager,
        interfaces.ISiteMenuItem)


class ContextSelectedChecker(ViewNameSelectedChecker):
    """Context menu item selected checker."""

    zope.component.adapts(zope.interface.Interface, IBrowserRequest,
        zope.interface.Interface, interfaces.IMenuManager,
        interfaces.IContextMenuItem)



