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
$Id: layer.py 197 2007-04-13 05:03:32Z rineichen $
"""
__docformat__ = "reStructuredText"

import zope.interface
from zope.traversing.api import getRoot
from zope.traversing.browser import absoluteURL

from zope.viewlet import viewlet
from zope.app.component import hooks
from zope.app.pagetemplate import ViewPageTemplateFile

from z3c.menu.ready2go import interfaces


# base menu item mixin
class MenuItem(viewlet.ViewletBase):
    """Menu item base."""

    template = ViewPageTemplateFile('item.pt')

    # set this attrs directly in zcml or override it in a sub class
    contextInterface = zope.interface.Interface
    viewInterface = zope.interface.Interface
    viewName = u'index.html'
    cssActive = u'selected'
    cssInActive = u''
    weight = 0
    subMenuProviderName = None

    # override it and use i18n msg ids
    @property
    def title(self):
        return self.__name__

    @property
    def css(self):
        if self.selected:
            return self.cssActive
        else:
            return self.cssInActive

    @property
    def available(self):
        return True

    @property
    def selected(self):
        """Selected if context and view interfaces compares."""
        if self.viewInterface.providedBy(self.__parent__) and \
            self.contextInterface.providedBy(self.__parent__.context):
            return True
        return False

    @property
    def url(self):
        context = self.getURLContext()
        return absoluteURL(context, self.request) + '/' + self.viewName

    @property
    def subProviderName(self):
        """Name of the sub item menu provider."""
        return self.subMenuProviderName

    def getURLContext(self):
        return getRoot(self.context)

    def render(self):
        """Return the template with the option 'menus'"""
        return self.template()

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.__name__)


class GlobalMenuItem(MenuItem):
    """Global menu item."""

    zope.interface.implements(interfaces.IGlobalMenuItem)

    @property
    def selected(self):
        if self.viewInterface.providedBy(self.__parent__) and \
            self.contextInterface.providedBy(self.__parent__.context):
            return True
        return False


class SiteMenuItem(MenuItem):
    """Site menu item."""

    zope.interface.implements(interfaces.IGlobalMenuItem)

    def getURLContext(self):
        return hooks.getSite()


class ContextMenuItem(MenuItem):
    """Context menu item."""

    zope.interface.implements(interfaces.IContextMenuItem)

    @property
    def selected(self):
        """Selected if also view name compares."""
        if self.viewInterface.providedBy(self.__parent__) and \
            self.contextInterface.providedBy(self.__parent__.context) and \
            self.__parent__.__name__ == self.viewName:
            return True
        return False

    def getURLContext(self):
        return self.context


class AddMenuItem(MenuItem):
    """Add menu item."""

    zope.interface.implements(interfaces.IAddMenuItem)

    @property
    def selected(self):
        return False

    @property
    def subProviderName(self):
        return None

    def getURLContext(self):
        return self.context
