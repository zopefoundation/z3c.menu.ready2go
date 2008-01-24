##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
$Id:$
"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.schema
import zope.configuration.fields
import zope.security.zcml
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserView

from zope.component import zcml

from z3c.i18n import MessageFactory as _
from z3c.menu.ready2go import interfaces
from z3c.menu.ready2go import checker


class IMenuSelectorDirective(zope.interface.Interface):
    """A directive to register a menu selector."""

    factory = zope.configuration.fields.GlobalObject(
        title=_("Selector factory"),
        description=_("Python name of a factory which can create the"
                      " selector object.  This must identify an"
                      " object in a module using the full dotted name."),
        required=False,
        default=checker.TrueSelectedChecker)

    for_ = zope.configuration.fields.GlobalObject(
        title=u"Context",
        description=u"The content interface or class this selector is for.",
        required=False)

    view = zope.configuration.fields.GlobalObject(
        title=_("The view the selector is registered for."),
        description=_("The view can either be an interface or a class. By "
                      "default the provider is registered for all views, "
                      "the most common case."),
        required=False,
        default=IBrowserView)

    layer = zope.configuration.fields.GlobalObject(
        title=_("The layer the view is in."),
        description=_("""
        A skin is composed of layers. It is common to put skin
        specific views in a layer named after the skin. If the 'layer'
        attribute is not supplied, it defaults to 'default'."""),
        required=False,
        default=IBrowserRequest)

    manager = zope.configuration.fields.GlobalObject(
        title=u"Menu Manager",
        description=u"The menu manager interface or class this selector is for.",
        required=False,
        default=interfaces.IMenuManager)

    menu = zope.configuration.fields.GlobalObject(
        title=u"Menu Item",
        description=u"The menu item interface or class this selector is for.",
        required=False,
        default=interfaces.IMenuItem)


# menu selector directive
def menuSelectorDirective(
    _context, factory=checker.TrueSelectedChecker,
    for_=zope.interface.Interface, layer=IBrowserRequest, view=IBrowserView,
    manager=interfaces.IMenuManager, menu=interfaces.IMenuItem):

    # Security map dictionary
    objs = (for_, layer, view, manager ,menu)
    factory = (factory,)

    zcml.adapter(_context, factory, provides=interfaces.ISelectedChecker,
        for_=objs, permission=None, name='', trusted=False, locate=False)
