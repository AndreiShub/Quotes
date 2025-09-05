from django.db import models
from django.core.exceptions import ValidationError

class Quote(models.Model):
    text = models.TextField(unique=True, error_messages={'unique': 'Такая цитата уже существует.'})
    source = models.CharField(max_length=255)
    weight = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def clean(self):
        if Quote.objects.filter(source=self.source).exclude(id=self.id).count() >= 3:
            raise ValidationError("У одного источника может быть максимум 3 цитаты.")

    def __str__(self):
        return f"{self.text[:30]}... ({self.source})"