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
"""Interfaces
"""
import zope.interface
import zope.schema
import zope.viewlet.interfaces

from z3c.menu.ready2go.i18n import MessageFactory as _


class IMenuManager(zope.viewlet.interfaces.IViewletManager):
    """Generic nenu manager."""

    def render():
        """Represent the menu"""


class IMenuItem(zope.viewlet.interfaces.IViewlet):
    """Menu item base."""

    template = zope.interface.Attribute("""Page template""")

    contextInterface = zope.interface.Attribute(
        """Context discriminator interface""")

    viewInterface = zope.interface.Attribute(
        """View discriminator interface""")

    title = zope.schema.TextLine(
        title=_('Title'),
        description=_('Menu item title'),
        default=''
    )

    viewName = zope.schema.TextLine(
        title=_('View name'),
        description=_('Name of the view which the menu points to.'),
        default=''
    )

    weight = zope.schema.TextLine(
        title=_('Weight'),
        description=_('Weight of the menu item order.'),
        default=''
    )

    cssActive = zope.schema.TextLine(
        title=_('Active CSS class name'),
        description=_('CSS class name for active menu items'),
        default=''
    )

    cssInActive = zope.schema.TextLine(
        title=_('In-Active CSS class name'),
        description=_('CSS class name for inactive menu items'),
        default=''
    )

    css = zope.schema.TextLine(
        title=_('CSS class name'),
        description=_('CSS class name'),
        default=''
    )

    available = zope.schema.Bool(
        title=_('Available'),
        description=_('Marker for available menu item'),
        default=True
    )

    selected = zope.schema.Bool(
        title=_('Selected'),
        description=_('Marker for selected menu item'),
        default=False
    )

    url = zope.schema.TextLine(
        title=_('URL'),
        description=_('URL or other url like javascript function.'),
        default=''
    )

    subMenuProviderName = zope.schema.TextLine(
        title=_('Sub menu provider name'),
        description=_('Name of the sub menu provider.'),
        default=''
    )

    def getURLContext():
        """Returns the context the base url."""

    def render():
        """Return the template with the option 'menus'"""


class ISelectedChecker(zope.interface.Interface):
    """Selected checker."""

    selected = zope.schema.Bool(
        title=_('Selected'),
        description=_('Marker for selected menu item'),
        default=False
    )


class IGlobalMenuItem(IMenuItem):
    """Menu item with ZODB application root as url base."""


class ISiteMenuItem(IMenuItem):
    """Menu item with nearest site as url base."""


class IContextMenuItem(IMenuItem):
    """Menu item with context as url base."""


class IAddMenuItem(IMenuItem):
    """Add menu item with context as url base."""
