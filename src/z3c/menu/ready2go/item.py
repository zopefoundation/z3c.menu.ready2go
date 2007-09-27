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
from zope.traversing.browser import absoluteURL
from zope.viewlet import viewlet
from zope.app.component import hooks
from zope.app.pagetemplate import ViewPageTemplateFile


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

    # override it and use i18n msg ids
    @property
    def title(self):
        return self.__name__

    @property
    def available(self):
        return True

    def getURLContext(self):
        return hooks.getSite()

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
        if self.viewInterface.providedBy(self.__parent__) and \
            self.contextInterface.providedBy(self.__parent__.context) and \
            self.__parent__.__name__ == self.viewName:
            return True
        return False

    @property
    def url(self):
        context = self.getURLContext()
        return absoluteURL(context, self.request) + '/' + self.viewName

    def render(self):
        """Return the template with the option 'menus'"""
        return self.template()

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.__name__)


class GlobalMenuItem(MenuItem):
    """Global menu item."""

    def getURLContext(self):
        return hooks.getSite()


class ContextMenuItem(MenuItem):
    """Context menu item."""

    def getURLContext(self):
        return self.context
