from django.contrib import admin
from .models import parties_detail, task, payment_installment

admin.site.register(parties_detail)
admin.site.register(task)
admin.site.register(payment_installment)