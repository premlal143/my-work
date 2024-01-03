from django.db import models
from master.models import base_table
from labor.models import labor_register

class parties_detail(base_table):
    labor_id = models.ForeignKey(labor_register, on_delete=models.CASCADE)
    firm_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.firm_name}"
    

class task(base_table):
    TASK_STATUS = (
        ('Pending','Task Pending'),
        ('Ongoing','Task On-Going'),
        ('Done','Task Done'),
    )

    PAYMENT_STATUS = (
        ('Pending', 'Payment Pending'),
        ('Done','Payment Done'),
        ('Partially Paid','Partially Paid'),
    )
    task_id = models.CharField(primary_key= True, max_length=50, blank=True)
    party_id = models.ForeignKey(parties_detail, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    total_payment = models.FloatField()
    task_status = models.CharField(choices=TASK_STATUS, default='Pending',max_length=50, blank=True)
    paid_payment = models.FloatField(default=0, blank=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=50, default='Pending', blank=True)

    def __str__(self):
        return self.task_id
    
    def save(self, *args, **kwargs):
        if not self.task_id:
            counters = counter_table.objects.get(id=1)
            counters.last_task_id += 1
            counters.save()
            self.task_id = str(self.party_id.labor_id) + "_" + str(counters.last_task_id)
        super(task, self).save(*args, **kwargs)