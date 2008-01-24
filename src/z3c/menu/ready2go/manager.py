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
import zope.security
from zope.viewlet import manager

from z3c.menu.ready2go import interfaces


def isAvailable(viewlet):
    try:
        return zope.security.canAccess(viewlet, 'render') and viewlet.approved
    except AttributeError:
        return True


class MenuManager(manager.ConditionalViewletManager):
    """Menu manager for all kind of menu items"""

    zope.interface.implements(interfaces.IMenuManager)

    def filter(self, viewlets):
        """Sort out all viewlets which are explicit not available

        ``viewlets`` is a list of tuples of the form (name, viewlet).
        """
        return [(name, viewlet) for name, viewlet in viewlets
                if isAvailable(viewlet)]


class EmptyMenuManager(object):
    """Empty menu manager."""

    zope.interface.implements(interfaces.IMenuManager)

    def __init__(self, context, request, view):
        self.__updated = False
        self.__parent__ = view
        self.context = context
        self.request = request

    def update(self):
        pass

    def render(self):
        return u''