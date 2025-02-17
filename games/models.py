from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    order = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ["-order"]

    def __str__(self):
        return self.title
