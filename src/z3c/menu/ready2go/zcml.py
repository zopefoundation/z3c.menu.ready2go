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
import zope.configuration.fields
import zope.security.checker
from zope.component import zcml
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserView
from zope.viewlet import viewlet
from zope.viewlet.metadirectives import IViewletDirective
from zope.app.publisher.browser import viewmeta

from z3c.i18n import MessageFactory as _
from z3c.menu.ready2go import interfaces
from z3c.menu.ready2go import checker
from z3c.menu.ready2go import item


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


class IMenuItemDirective(IViewletDirective):
    """Menu item directive."""

    title = zope.configuration.fields.MessageID(
        title=u"I18n title",
        description=u"Translatable title for a viewlet.",
        required=False)

# Arbitrary keys and values are allowed to be passed to the menu item.
IMenuItemDirective.setTaggedValue('keyword_arguments', True)


# menuItem directive
def menuItemDirective(
    _context, name, permission, for_=zope.interface.Interface,
    layer=IDefaultBrowserLayer, view=IBrowserView,
    manager=interfaces.IMenuManager, class_=None, template=None,
    attribute='render', allowed_interface=None, allowed_attributes=None,
    title=None, **kwargs):

    # Security map dictionary
    required = {}

    if title is not None:
        # set i18n aware title
        kwargs['i18nTitle'] = title

    # Get the permission; mainly to correctly handle CheckerPublic.
    permission = viewmeta._handle_permission(_context, permission)

    # Either the class or template must be specified.
    if not (class_ or template):
        raise ConfigurationError("Must specify a class or template")

    # Make sure that all the non-default attribute specifications are correct.
    if attribute != 'render':
        if template:
            raise ConfigurationError(
                "Attribute and template cannot be used together.")

        # Note: The previous logic forbids this condition to evere occur.
        if not class_:
            raise ConfigurationError(
                "A class must be provided if attribute is used")

    # Make sure that the template exists and that all low-level API methods
    # have the right permission.
    if template:
        template = os.path.abspath(str(_context.path(template)))
        if not os.path.isfile(template):
            raise ConfigurationError("No such file", template)
        required['__getitem__'] = permission

    # Make sure the has the right form, if specified.
    if class_:
        if attribute != 'render':
            if not hasattr(class_, attribute):
                raise ConfigurationError(
                    "The provided class doesn't have the specified attribute "
                    )
        if template:
            # Create a new class for the viewlet template and class.
            new_class = viewlet.SimpleViewletClass(
                template, bases=(class_, ), attributes=kwargs, name=name)
        else:
            if not hasattr(class_, 'browserDefault'):
                cdict = {'browserDefault':
                         lambda self, request: (getattr(self, attribute), ())}
            else:
                cdict = {}

            cdict['__name__'] = name
            cdict['__page_attribute__'] = attribute
            cdict.update(kwargs)
            new_class = type(class_.__name__,
                             (class_, viewlet.SimpleAttributeViewlet), cdict)

        if hasattr(class_, '__implements__'):
            zope.interface.classImplements(new_class, IBrowserPublisher)

    else:
        # Create a new class for the viewlet template alone.
        new_class = viewlet.SimpleViewletClass(template, name=name,
                                               attributes=kwargs)

    # Set up permission mapping for various accessible attributes
    viewmeta._handle_allowed_interface(
        _context, allowed_interface, permission, required)
    viewmeta._handle_allowed_attributes(
        _context, allowed_attributes, permission, required)
    viewmeta._handle_allowed_attributes(
        _context, kwargs.keys(), permission, required)
    viewmeta._handle_allowed_attributes(
        _context,
        (attribute, 'browserDefault', 'update', 'render', 'publishTraverse'),
        permission, required)

    # Register the interfaces.
    viewmeta._handle_for(_context, for_)
    zcml.interface(_context, view)

    # Create the security checker for the new class
    zope.security.checker.defineChecker(new_class,
        zope.security.checker.Checker(required))

    # register viewlet
    _context.action(
        discriminator = ('viewlet', for_, layer, view, manager, name),
        callable = zcml.handler,
        args = ('registerAdapter',
                new_class, (for_, layer, view, manager),
                zope.viewlet.interfaces.IViewlet, name, _context.info),)


def addMenuItemDirective(_context, name, permission,
    for_=zope.interface.Interface, layer=IDefaultBrowserLayer,
    view=IBrowserView, manager=interfaces.IMenuManager,
    class_=item.AddMenuItem, template=None, attribute='render',
    allowed_interface=None, allowed_attributes=None, title=None, **kwargs):
    menuItemDirective(_context, name, permission, for_, layer, view, manager,
        class_, template, attribute, allowed_interface, allowed_attributes,
        title, **kwargs)


def contextMenuItemDirective(_context, name, permission,
    for_=zope.interface.Interface, layer=IDefaultBrowserLayer,
    view=IBrowserView, manager=interfaces.IMenuManager,
    class_=item.ContextMenuItem,template=None, attribute='render',
    allowed_interface=None, allowed_attributes=None, title=None, **kwargs):
    menuItemDirective(_context, name, permission, for_, layer, view, manager,
        class_, template, attribute, allowed_interface, allowed_attributes,
        title, **kwargs)


def globalMenuItemDirective(_context, name, permission,
    for_=zope.interface.Interface, layer=IDefaultBrowserLayer,
    view=IBrowserView, manager=interfaces.IMenuManager,
    class_=item.GlobalMenuItem, template=None, attribute='render',
    allowed_interface=None, allowed_attributes=None, title=None, **kwargs):
    menuItemDirective(_context, name, permission, for_, layer, view, manager,
        class_, template, attribute, allowed_interface, allowed_attributes,
        title, **kwargs)


def siteMenuItemDirective(_context, name, permission,
    for_=zope.interface.Interface, layer=IDefaultBrowserLayer,
    view=IBrowserView, manager=interfaces.IMenuManager,
    class_=item.SiteMenuItem, template=None, attribute='render',
    allowed_interface=None, allowed_attributes=None, title=None, **kwargs):
    menuItemDirective(_context, name, permission, for_, layer, view, manager,
        class_, template, attribute, allowed_interface, allowed_attributes,
        title, **kwargs)


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
