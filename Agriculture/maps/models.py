from django.db import models
from Users.models import Details

class Field(models.Model):
    field_name = models.CharField(max_length=100, unique=True)
    coordinates = models.JSONField()
    created_by = models.ForeignKey(Details, on_delete=models.SET_NULL, null=True, related_name="fields_created")
    updated_by = models.ForeignKey(Details, on_delete=models.SET_NULL, null=True, blank=True, related_name="fields_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.field_name

# NEW MODEL FOR BLOCKS
class Block(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="blocks")
    block_name = models.CharField(max_length=100)
    coordinates = models.JSONField() # Holds the sub-polygon coordinates for this specific block
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('field', 'block_name') # Prevents duplicate block names inside the same field

    def __str__(self):
        return f"{self.field.field_name} - {self.block_name}"