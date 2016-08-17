django-rest-framework-roles
===========================

Simplifies `Role Based Access Control`_ in `django-rest-framework`_.

Why would I use this?
---------------------

You have more than one type of user in your data model and you have
business logic that diverges depending on the type of user. You do not
want to organize your API by role because that is not very RESTful. You
do not want to manually type out a lot of conditional branching around
user roles.

Modeling Requirements
---------------------

-  You must have one **Group** for each role
-  A **User** cannot belong to more than one of the **Groups**
   corresponding to each role

Installation
------------

.. code:: bash

    $ pip install django-rest-framework-roles

Configuration
-------------

-  ``VIEWSET_METHOD_REGISTRY`` A tuple of DRF methods to override.
   Defaults to:

.. code:: python

        (
            "get_queryset",
            "get_serializer_class",
            "perform_create",
            "perform_update",
            "perform_destroy",
        )

-  ``ROLE_GROUPS`` A tuple of Group names that correspond 1-to-1 with
   user roles. Defaults to:

.. code:: python

        [group.name.lower() for group in Group.objects.all()]

Usage
-----

Add the mixin to any ViewSet:

.. code:: python

    from drf_roles import RoleViewSetMixin

    class MyViewSet(RoleViewSetMixin, ModelViewSet):
        # ...

For each of the methods specified in ``VIEWSET_METHOD_REGISTRY`` a
role-scoped method will be generated on your ViewSet.

Parameterizing
~~~~~~~~~~~~~~

For example, let’s say you have three groups named *Takers*, *Leavers* &
*Gods*. Let’s also say you included ``"get_queryset"`` in the
``ROLE_REGISTRY``.

When a *Taker* user hits an endpont on the ViewSet, the call to
``get_queryset`` will be rerouted to a call to
``get_queryset_for_takers``.

When a *Leaver* user hits an endpont on the ViewSet, the call to
``get_queryset`` will be rerouted to a call to
``get_queryset_for_leavers``.

When a *God* user hits an endpont on the ViewSet, the call to
``get_queryset`` will be rerouted to a call to
``get_queryset_for_gods``.

You can implement each of these methods on your ViewSet to return a
different queryset for each type of user.

Not Parameterizing
~~~~~~~~~~~~~~~~~~

You can also *not* implement one or more of these methods, in which case
the default call will be executed. For example, with our same set of
groups and with ``"get_serializer_class"`` included in the role
registry, let’s say you did not implement
``get_serializer_class_for_takers``. When a *Taker* user hits an
endpoint on the ViewSet, the default implementation of
``get_serializer_class`` will be executed and return
``serializer_class``.

In this case, you would want to be sure that you have a
``serializer_class`` defined on your ViewSet! Otherwise Django REST
Framework will complain. It is a good idea to always define a default
``queryset`` and ``serializer_class`` with least privilege (e.g:
Model.objects.none()).

Roadmap
-------

-  Some projects require even further parameterization. For example, you may need
   to use a different `serializer_class` depending on the user's *role* **and**
   the *request method*.
- There may be a more pleasant way to express the parameterization in code. For
  example, it may be more pleasing to use nested classes instead of renaming the
  methods.

.. _Role Based Access Control: https://en.wikipedia.org/wiki/Role-based_access_control
.. _django-rest-framework: http://www.django-rest-framework.org/
