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

    # internal approved values
    approved = False
    approvedURL = None

    # url view name if different then ``selected`` viewName
    viewName = u'index.html'

    # ``selected`` discriminator values
    contextInterface = zope.interface.Interface
    viewInterface = zope.interface.Interface
    selectedViewName = viewName

    # css classes
    cssActive = u'selected'
    cssInActive = u''

    # menu order weight
    weight = 0

    # sub menu provider name
    subMenuProviderName = None

    def __init__(self, context, request, view, manager):
        super(MenuItem, self).__init__(context, request, view, manager)
        self.view = view
        self.setupFilter()

    def setupFilter(self):
        """Catch location error and set approved attributes.
        
        Note, this get called before update because the filter method in menu 
        manager needs to know that before the menu items update method get 
        called.
        """
        try:
            if self.available:
                self.approvedURL = self.url
                self.approved = True
        except TypeError:
            self.approvedURL = None
            self.approved = False

    # override it and use i18n msg ids
    @property
    def title(self):
        return self.__name__

    @property
    def css(self):
        """Return cssActive, cssInActive or None. 

        None will not render a HTML attribute in TAL.
        """
        if self.selected and self.cssActive:
            return self.cssActive
        elif self.selected and self.cssInActive:
            return self.cssInActive
        else:
            return None

    @property
    def available(self):
        """Available checker call"""
        return True

    @property
    def selected(self):
        """Selected checker call"""
        checker = zope.component.getMultiAdapter((self.context, self.request,
            self.view, self.manager, self), interfaces.ISelectedChecker)
        return checker.selected

    @property
    def url(self):
        return '%s/%s' % (absoluteURL(self.getURLContext(), self.request),
            self.viewName)

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


class SiteMenuItem(MenuItem):
    """Site menu item."""

    zope.interface.implements(interfaces.ISiteMenuItem)

    def getURLContext(self):
        return hooks.getSite()


class ContextMenuItem(MenuItem):
    """Context menu item."""

    zope.interface.implements(interfaces.IContextMenuItem)

    def getURLContext(self):
        return self.context


class AddMenuItem(MenuItem):
    """Add menu item."""

    zope.interface.implements(interfaces.IAddMenuItem)

    subMenuProviderName = None

    @property
    def selected(self):
        return False

    def getURLContext(self):
        return self.context