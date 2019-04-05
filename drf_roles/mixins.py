from django.conf import settings
from django.contrib.auth.models import Group

# Default settings
DEFAULT_REGISTRY = (
    "get_queryset",
    "get_serializer_class",
    "perform_create",
    "perform_update",
    "perform_destroy",
)


class RoleError(Exception):
    """Base class for exceptions in this module."""
    pass


class RoleViewSetMixin(object):
    """A ViewSet mixin that parameterizes DRF methods over roles"""
    _viewset_method_registry = set(getattr(settings, "VIEWSET_METHOD_REGISTRY", DEFAULT_REGISTRY))

    def __init__(self, **_kwargs):
        groups = getattr(settings, "ROLE_GROUPS", None)
        if groups is None:
            groups = [group.name.lower() for group in Group.objects.all()]
        self._role_groups = set(groups)

    def _call_role_fn(self, fn, *args, **kwargs):
        """Attempts to call a role-scoped method"""
        try:
            role_name = self._get_role(self.request.user)
            role_fn = "{}_for_{}".format(fn, role_name)
            return getattr(self, role_fn)(*args, **kwargs)
        except (AttributeError, RoleError):
            return getattr(super(RoleViewSetMixin, self), fn)(*args, **kwargs)

    def _get_role(self, user):
        """Retrieves the given user's role"""
        user_groups = set([group.name.lower() for group in user.groups.all()])
        user_role = self._role_groups.intersection(user_groups)

        if len(user_role) < 1:
            raise RoleError("The user is not a member of any role groups")
        elif len(user_role) > 1:
            raise RoleError("The user is a member of multiple role groups")
        else:
            return user_role.pop()

def register_fn(fn):
    """Dynamically adds fn to RoleViewSetMixin"""
    def inner(self, *args, **kwargs):
        return self._call_role_fn(fn, *args, **kwargs)
    setattr(RoleViewSetMixin, fn, inner)

# Registers whitelist of ViewSet fns to override
for fn in RoleViewSetMixin._viewset_method_registry:
    register_fn(fn)
