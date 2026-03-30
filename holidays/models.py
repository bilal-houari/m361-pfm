from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    @property
    def duration(self):
        diff = self.end_date - self.start_date
        return diff.days + 1
