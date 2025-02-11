from mptt.managers import TreeManager
from mptt.querysets import TreeQuerySet
from parler.managers import TranslatableManager, TranslatableQuerySet


class MenuItemQuerySet(TranslatableQuerySet, TreeQuerySet):

    def as_manager(cls):
        # make sure creating managers from querysets works.
        manager = MenuItemManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class MenuItemManager(TreeManager, TranslatableManager):
    _queryset_class = MenuItemQuerySet
