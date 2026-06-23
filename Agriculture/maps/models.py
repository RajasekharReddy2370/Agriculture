from django.db import models
from Users.models import Details


class Field(models.Model):

    field_name = models.CharField(
        max_length=100,
        unique=True
    )

    coordinates = models.JSONField()

    created_by = models.ForeignKey(
        Details,
        on_delete=models.SET_NULL,
        null=True,
        related_name="fields_created"
    )

    updated_by = models.ForeignKey(
        Details,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fields_updated"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.field_name