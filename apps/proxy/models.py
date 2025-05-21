from django.db import models
import uuid
from django_extensions.db.models import TimeStampedModel

class ChildcareCRMToken(models.Model):
    access_token = models.TextField()

    # Singleton pattern
    def save(self, *args, **kwargs):
        self.pk = 1  # always force a single row
        super().save(*args, **kwargs)

    @classmethod
    def get_token(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class School(TimeStampedModel):
    internal_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255, default=None, null=True)
    crm_id = models.IntegerField(default=None, null=True)

    def __str__(self):
        return f"{self.name} - {self.crm_id}"

class AvailabilitySlot(TimeStampedModel):
    internal_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='availability_slots'
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    start_datetime_raw = models.CharField(max_length=64, default=None, null=True)
    end_datetime_raw = models.CharField(max_length=64, default=None, null=True)
    is_available = models.BooleanField(default=True)
    length = models.IntegerField(help_text="Duration of the slot in minutes")

    def __str__(self):
        return f"{self.start_datetime} - {self.end_datetime} ({'Available' if self.is_available else 'Unavailable'})"