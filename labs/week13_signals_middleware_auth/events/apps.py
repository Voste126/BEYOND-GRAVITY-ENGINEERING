"""Events app configuration.

STUB: Import receivers in ``ready()`` to connect signal handlers.
"""

from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

    def ready(self) -> None:
        """Import receivers module to register signal handlers.

        TODO: Add this import line:
            import events.receivers  # noqa: F401
        """
        pass  # TODO: import events.receivers here
