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
from zope.traversing.browser import absoluteURL
from zope.viewlet import manager
from zope.app.component import hooks
from zope.app.pagetemplate import ViewPageTemplateFile


def getWeight((name, viewlet)):
    try:
        return int(viewlet.weight)
    except AttributeError:
        return 0


# base menu manager mixin
class MenuManager(manager.ViewletManagerBase):
    """Menu manager for all kind of menu items"""

    def sort(self, viewlets):
        return sorted(viewlets, key=getWeight)

    def filter(self, viewlets):
        """Filter available menu items."""
        # Only return viewlets accessible to the principal
        return [(name, viewlet) for name, viewlet in viewlets
                if zope.security.canAccess(viewlet, 'render') and
                viewlet.available == True]

    def render(self):
        """Return the template whihc renders the menu items."""
        if not self.viewlets:
            return u''
        return self.template()

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.__name__)
