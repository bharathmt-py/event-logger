from django.db import models

class LogEntry(models.Model):
    message = models.TextField()
    source = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.isoformat()} - {self.source or 'unknown'}"