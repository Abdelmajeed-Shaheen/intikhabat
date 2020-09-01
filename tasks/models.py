from django.db import models
from users_management.models import (UserProfile)
from adminstration.models import Comittee
# Create your models here.
class ComitteeTask(models.Model):
    description=models.TextField()
    notes=models.TextField(null=True,blank=True)
    is_complete=models.BooleanField()
    created_by=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comittee=models.ForeignKey(Comittee, on_delete=models.CASCADE)
    title=models.CharField(default="يرجى تعيين عنوان المهمة", max_length=50)
    def __str__(self):
        return str(self.title)
