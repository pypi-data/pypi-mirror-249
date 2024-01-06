from django.db import models
from django.db.models import Model
from logs.models.fields import (
    CreatingUserField,
    CreatingSessionKeyField,
    LastUserField,
    LastSessionKeyField,
)


class AuthStampedModel(Model):
    """
    An abstract base class model that provides auth and session information
    fields.
    """

    created_by = CreatingUserField(
        verbose_name="created by",
        related_name="created_%(app_label)s_%(class)s_set",
        on_delete=models.SET_NULL,
    )
    created_with_session_key = CreatingSessionKeyField(_("created with session key"))
    modified_by = LastUserField(
        verbose_name="modified by",
        related_name="modified_%(app_label)s_%(class)s_set",
        on_delete=models.SET_NULL,
    )
    modified_with_session_key = LastSessionKeyField("modified with session key")

    class Meta:
        abstract = True
