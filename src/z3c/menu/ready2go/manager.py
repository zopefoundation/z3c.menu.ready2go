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
from zope.viewlet import manager

from z3c.menu.ready2go import interfaces


class MenuManager(manager.ConditionalViewletManager):
    """Menu manager for all kind of menu items"""

    zope.interface.implements(interfaces.IMenuManager)


class EmptyMenuManager(object):
    """Empty menu manager."""

    zope.interface.implements(interfaces.IMenuManager)

    def update(self):
        pass

    def render(self):
        return u''