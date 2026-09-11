"""factory_boy factories for Week 13 tests.

These are PROVIDED — do not modify.  They create test data for
signals, middleware, and auth backend tests.
"""

from __future__ import annotations

import factory
from django.contrib.auth import get_user_model

from accounts.models import Membership, Organization
from events.models import LaunchEvent

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):  # type: ignore[override]
        password = kwargs.pop("password", "testpass123")
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(password)
        user.save()
        return user


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Org {n}")
    slug = factory.Sequence(lambda n: f"org-{n}")


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    role = Membership.Role.MEMBER


class LaunchEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LaunchEvent

    name = factory.Sequence(lambda n: f"Launch Event {n}")
    date = factory.LazyFunction(lambda: "2025-06-15")
    location = "Cape Canaveral"
    status = "scheduled"
