import typing as t
import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from .settings import DEFAULT_VERSION, versioning_is_disabled


class ModelVersion(models.Model):
    version_id = models.UUIDField(editable=False)
    version = models.IntegerField(
        default=DEFAULT_VERSION, validators=[MinValueValidator(DEFAULT_VERSION)], editable=False
    )
    version_created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        unique_together = ["version_id", "version"]

    @staticmethod
    def versioning_enabled() -> bool:
        return not versioning_is_disabled.get()

    def save(self, *args: t.Any, **kwargs: t.Any) -> None:
        # new record is being created
        if self.version_id is None:
            self.version_id = uuid.uuid4()
        # old record, updating version number
        elif self.pk is not None and self.versioning_enabled():
            self._copy_current_instance()
            self._update_version()
        super().save(*args, **kwargs)

    def _update_version(self) -> None:
        max_available_version = self.__class__.objects.filter(
            version_id=self.version_id
        ).aggregate(models.Max("version"))
        self.version = max_available_version["version__max"] + 1
        self.version_created_at = timezone.now()

    def _copy_current_instance(self) -> None:
        instance_before_changes = self.__class__.objects.get(pk=self.pk)
        instance_before_changes.pk = None
        instance_before_changes._state.adding = True
        instance_before_changes.save()
