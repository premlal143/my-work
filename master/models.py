from django.db import models

class base_table(models.Model):
    Created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class meta:
        abstract = True

# Create your models here.
class counter_table(base_table):
    last_labor_id = models.IntegerField(default=0)
    last_task_id = models.IntegerField(default=0)