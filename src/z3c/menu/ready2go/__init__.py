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

from z3c.menu.ready2go import interfaces


class IGlobalMenu(interfaces.IMenuManager):
    """CSS viewlet manager."""


class ISiteMenu(interfaces.IMenuManager):
    """CSS viewlet manager."""


class IContextMenu(interfaces.IMenuManager):
    """CSS viewlet manager."""


class IAddMenu(interfaces.IMenuManager):
    """CSS viewlet manager."""
