===============
Ready 2 go Menu
===============

The z3c.menu.ready2go package provides a menu implementation which allows you 
to implement menus based on content providers and viewlets.

Let's see what this means.


Global Menu
-----------

Let's create some menu and register them as viewlet manager:

  >>> from zope.viewlet.interfaces import IViewlet
  >>> from zope.viewlet import manager
  >>> from z3c.menu.ready2go import interfaces
  >>> from z3c.menu.ready2go import IGlobalMenu
  >>> from z3c.menu.ready2go import ISiteMenu
  >>> from z3c.menu.ready2go import IContextMenu
  >>> from z3c.menu.ready2go import IAddMenu
  >>> from z3c.menu.ready2go.manager import MenuManager

  >>> GlobalMenu = manager.ViewletManager('left', IGlobalMenu,
  ...     bases=(MenuManager,))

  >>> SiteMenu = manager.ViewletManager('left', ISiteMenu,
  ...     bases=(MenuManager,))

  >>> ContextMenu = manager.ViewletManager('left', IContextMenu,
  ...     bases=(MenuManager,))

  >>> AddMenu = manager.ViewletManager('left', IAddMenu,
  ...     bases=(MenuManager,))

Our menu managers implement IMenuManager:

  >>> interfaces.IMenuManager.implementedBy(GlobalMenu)
  True

  >>> interfaces.IMenuManager.implementedBy(SiteMenu)
  True

  >>> interfaces.IMenuManager.implementedBy(ContextMenu)
  True

  >>> interfaces.IMenuManager.implementedBy(AddMenu)
  True

Now we have to define a context:

  >>> import zope.interface
  >>> from zope.app.container import contained
  >>> from zope.app.container.interfaces import IContained
  >>> class Content(contained.Contained):
  ...     zope.interface.implements(IContained)
  >>> root['content'] = Content()
  >>> content = root['content']

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

And we need a view:

  >>> from zope.publisher.interfaces.browser import IBrowserView
  >>> class View(contained.Contained):
  ... 
  ...     zope.interface.implements(IBrowserView)
  ... 
  ...     def __init__(self, context, request):
  ...         self.__parent__ = context
  ...         self.context = context
  ...         self.request = request

  >>> view = View(content, request)

Our menus can adapt the context, request and view:

  >>> globalMenu = GlobalMenu(content, request, view)
  >>> globalMenu.update()
  >>> globalMenu.render()
  u''

  >>> siteMenu = SiteMenu(content, request, view)
  >>> siteMenu.update()
  >>> siteMenu.render()
  u''

  >>> contextMenu = ContextMenu(content, request, view)
  >>> contextMenu.update()
  >>> contextMenu.render()
  u''

  >>> addMenu = AddMenu(content, request, view)
  >>> addMenu.update()
  >>> addMenu.render()
  u''


Global Menu Item
----------------


But now we register a context menu item for the IMenu:

  >>> import zope.component
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer

  >>> from z3c.menu.ready2go.item import GlobalMenuItem
  >>> class RootMenuItem(GlobalMenuItem):
  ...
  ...     viewName = 'root.html'

Now we need a security checker for our menu item

  >>> from zope.security.checker import NamesChecker, defineChecker
  >>> viewletChecker = NamesChecker(('update', 'render'))
  >>> defineChecker(RootMenuItem, viewletChecker)

  >>> zope.component.provideAdapter(
  ...     RootMenuItem,
  ...     (zope.interface.Interface, IDefaultBrowserLayer,
  ...     IBrowserView, IGlobalMenu),
  ...     IViewlet, name='RootMenuItem')

Now let's render the global menu again:

  >>> globalMenu.update()
  >>> print globalMenu.render()
  <li class="selected">
    <a href="http://127.0.0.1/root.html"><span>RootMenuItem</span></a>
  </li>
