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

import zope.interface
import zope.schema
from zope.viewlet import interfaces

from z3c.i18n import MessageFactory as _


class IMenuManager(interfaces.IViewletManager):
    """Generic nenu manager."""

    def render():
        """Represent the menu"""


class IMenuItem(interfaces.IViewlet):
    """Menu item base."""

    template = zope.interface.Attribute("""Page template""")

    contextInterface = zope.interface.Attribute(
        """Context discriminator interface""")

    viewInterface = zope.interface.Attribute(
        """View discriminator interface""")

    title = zope.schema.TextLine(
        title=_('Title'),
        description=_('Menu item title'),
        default=u''
        )

    viewName = zope.schema.TextLine(
        title=_('View name'),
        description=_('Name of the view which the menu points to.'),
        default=u''
        )

    weight = zope.schema.TextLine(
        title=_('Weight'),
        description=_('Weight of the menu item order.'),
        default=u''
        )

    cssActive = zope.schema.TextLine(
        title=_('Active CSS class name'),
        description=_('CSS class name for active menu items'),
        default=u''
        )

    cssInActive = zope.schema.TextLine(
        title=_('In-Active CSS class name'),
        description=_('CSS class name for inactive menu items'),
        default=u''
        )

    css = zope.schema.TextLine(
        title=_('CSS class name'),
        description=_('CSS class name'),
        default=u''
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
        default=u''
        )

    subMenuProviderName = zope.schema.TextLine(
        title=_('Sub menu provider name'),
        description=_('Name of the sub menu provider.'),
        default=u''
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
