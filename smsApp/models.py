from django.db import models

class SMSStatistic(models.Model):
    filed_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Filed: {self.filed_count}, Success: {self.success_count}"
