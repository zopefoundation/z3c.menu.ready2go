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

And we configure our menu item as viewlet Managers. This is normaly done by the
``viewletManager`` ZCML directive:

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

We also need our checker adapter which can check if a menu item is available
and/or selected:

  >>> import zope.component
  >>> from z3c.menu.ready2go import checker
  >>> zope.component.provideAdapter(checker.GlobalSelectedChecker)
  >>> zope.component.provideAdapter(checker.SiteSelectedChecker)
  >>> zope.component.provideAdapter(checker.ContextSelectedChecker)

Now we have to define a site and a context:

  >>> import zope.interface
  >>> from zope.app.container import contained
  >>> from zope.app.container import btree
  >>> from zope.app.container.interfaces import IContained
  >>> from zope.location.interfaces import IPossibleSite
  >>> from zope.app.component.site import SiteManagerContainer
  >>> from zope.app.component.site import LocalSiteManager

  >>> class Site(btree.BTreeContainer, SiteManagerContainer):
  ...     zope.interface.implements(IPossibleSite)
  ...     def __init__(self):
  ...         super(Site, self).__init__()
  ...         self.setSiteManager(LocalSiteManager(self))

  >>> class Content(contained.Contained):
  ...     zope.interface.implements(IContained)

  >>> root['site'] = Site()
  >>> site = root['site']

Now we have to set the site object as site. This is normaly done by the 
traverser but we do this here with the hooks helper because we do not really
traaverse to the site within the publisher/traverser:

  >>> from zope.app.component import hooks
  >>> hooks.setSite(site)

  >>> site['content'] = Content()
  >>> content = site['content']

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

And we need a view which knows about it's parent:

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

Our menus can adapt the context, request and view. See IViewletManager in
zope.viewlet for more infos about this pattern. If we render them, there is an
empty string returned. This means the menus don't find menu items for rendering:

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

Now we register a context menu item for our IGlobalMenu:

  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer

  >>> from z3c.menu.ready2go.item import GlobalMenuItem
  >>> class MyGlobalMenuItem(GlobalMenuItem):
  ...
  ...     viewName = 'root.html'

Now we need a security checker for our menu item

  >>> from zope.security.checker import NamesChecker, defineChecker
  >>> viewletChecker = NamesChecker(('update', 'render'))
  >>> defineChecker(MyGlobalMenuItem, viewletChecker)

And we configure our menu item for IGlobalMenu. This is normaly done by the
``viewlet`` ZCML directive:

  >>> zope.component.provideAdapter(
  ...     MyGlobalMenuItem,
  ...     (zope.interface.Interface, IDefaultBrowserLayer,
  ...     IBrowserView, IGlobalMenu),
  ...     IViewlet, name='My Global')

Now let's render the global menu again. You can see that we ve got a menu item:

  >>> globalMenu.update()
  >>> print globalMenu.render()
  <li>
    <a href="http://127.0.0.1/root.html"><span>My Global</span></a>
  </li>


Site Menu Item
--------------

Now we register a context menu item for our ISiteMenu:

  >>> import zope.component
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer

  >>> from z3c.menu.ready2go.item import SiteMenuItem
  >>> class MySiteMenuItem(SiteMenuItem):
  ...
  ...     viewName = 'site.html'

Now we need a security checker for our menu item

  >>> from zope.security.checker import NamesChecker, defineChecker
  >>> viewletChecker = NamesChecker(('update', 'render'))
  >>> defineChecker(MySiteMenuItem, viewletChecker)

And we configure our menu item for ISiteMenu. This is normaly done by the
``viewlet`` ZCML directive:

  >>> zope.component.provideAdapter(
  ...     MySiteMenuItem,
  ...     (zope.interface.Interface, IDefaultBrowserLayer,
  ...     IBrowserView, ISiteMenu),
  ...     IViewlet, name='My Site')

Now let's render the site menu again. You can see that we ve got a menu item
and the url points to our site:

  >>> siteMenu.update()
  >>> print siteMenu.render()
  <li>
    <a href="http://127.0.0.1/site/site.html"><span>My Site</span></a>
  </li>


Context Menu Item
-----------------

Now we register a context menu item for our IContextMenu:

  >>> import zope.component
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer

  >>> from z3c.menu.ready2go.item import ContextMenuItem
  >>> class MyContextMenuItem(ContextMenuItem):
  ...
  ...     viewName = 'context.html'

Now we need a security checker for our menu item

  >>> from zope.security.checker import NamesChecker, defineChecker
  >>> viewletChecker = NamesChecker(('update', 'render'))
  >>> defineChecker(MyContextMenuItem, viewletChecker)

And we configure our menu item for IContextMenu. This is normaly done by the
``viewlet`` ZCML directive:

  >>> zope.component.provideAdapter(
  ...     MyContextMenuItem,
  ...     (zope.interface.Interface, IDefaultBrowserLayer,
  ...     IBrowserView, IContextMenu),
  ...     IViewlet, name='My Context')

Now let's render the context menu again. You can see that we ve got a menu 
item. Another important point here is, that the url of such ContextMemuItem
implementations point to the context of the view:

  >>> contextMenu.update()
  >>> print contextMenu.render()
  <li>
    <a href="http://127.0.0.1/site/content/context.html"><span>My Context</span></a>
  </li>

Let's set the view  __name__ to ``context.html``. This will reflect that
the view offers the same name that our context menu needs to get rendered as
selected:

  >>> view.__name__ = 'context.html'

Now try again and see if the context menu titem get rendered as selected:

  >>> contextMenu.update()
  >>> print contextMenu.render()
  <li class="selected">
    <a href="http://127.0.0.1/site/content/context.html"><span>My Context</span></a>
  </li>


Menu groups
-----------

The global and the site menu items are grouped menu items. This means such menu
items should get rendered as selected if a context menu item is selected. This
reflects the menu hierarchie. Let's show how we can solve this not so simple 
problem. We offer a ISelectedChecker adapter which can decide if a menu get 
rendered as selected or not. This is very usefull because normaly a menu get 
registered and later we add views and can not change the menu item 
implementation. Let's see how such an adapter can handle an existing menu, 
context and view setup and change the selected rendering. We register a 
selected checker for our site menu item:

  >>> zope.component.provideAdapter(checker.TrueSelectedChecker,
  ...     (IContained, IDefaultBrowserLayer, None, ISiteMenu, MySiteMenuItem),
  ...     interfaces.ISelectedChecker)

Now we can render the site menu again. Note that our context is still the
sample content object.

  >>> siteMenu.update()
  >>> print siteMenu.render()
  <li class="selected">
    <a href="http://127.0.0.1/site/site.html"><span>My Site</span></a>
  </li>

This reflects that the site menu is a group menu which the context menu item 
of the content object is selected too.

  >>> contextMenu.update()
  >>> print contextMenu.render()
  <li class="selected">
    <a href="http://127.0.0.1/site/content/context.html"><span>My Context</span></a>
  </li>


Special use case
----------------

We have some special use case because of Zope's internals. One important part
is that our menu heavy depend on context and it's __parent__ chain to the 
zope application root. This is not allways supported by Zopes default setup.
One part is the bad integrated application control part which fakes a root
object which doesn't know about the real childs of the real root from the 
ZODB e.g. application root. Now we will show you that our menu by default
render no items if we get such a fake root which messes up our menu structure.

Let's define a object which does not know about any __parent__.

  >>> nirvana = Content()
  >>> nirvanaView = View(nirvana, request)

Now we can check what's happen to the menus if we adapt the parent less nirvana
context and update and render the menus. You can see that the global menu does
not contain any menu item. That's because the global menu items tries to find
the root by traversing from the context to the root by the __parent__ chain
and we don't support any parent for your nirvana object:

  >>> globalMenu = GlobalMenu(nirvana, request, nirvanaView)
  >>> globalMenu.update()
  >>> globalMenu.render()
  u''

But you can see that the site menu renders the menu item becyuse we lookup the 
site by the hooks and we still point to our site we set with setSite():

  >>> siteMenu = SiteMenu(nirvana, request, nirvanaView)
  >>> siteMenu.update()
  >>> print siteMenu.render()
  <li class="selected">
    <a href="http://127.0.0.1/site/site.html"><span>My Site</span></a>
  </li>


  >>> contextMenu = ContextMenu(nirvana, request, nirvanaView)
  >>> contextMenu.update()
  >>> contextMenu.render()
  u''

  >>> addMenu = AddMenu(nirvana, request, nirvanaView)
  >>> addMenu.update()
  >>> addMenu.render()
  u''
