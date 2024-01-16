from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from master.models import base_table,counter_table
from master.utils.unique import generate_password
# Create your models here.
class labor_register(base_table):
    labor_id = models.CharField(primary_key =True, max_length=50, blank=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=255 ,blank=True)
    credential_is_sent = models.BooleanField(default=False)
    otp = models.CharField(max_length=50, default="569864")


    def __str__(self):
        return f"{self.labor_id} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.labor_id:
            counters = counter_table.objects.get(id=3)
            counters.last_labor_id +=1
            counters.save()
            print(counters.last_labor_id)
            self.labor_id ='LB000' + str(counters.last_labor_id)
            print(self.labor_id)

        if not self.password:
            self.password = generate_password.generate_unique_password()

        if not self.credential_is_sent:
            subject = f'Labor Login Credential for {self.first_name} {self.last_name} at My-Work'
            message = f'Login ID :{self.labor_id} \nPasscode : {self.password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [f'{self.email}']
           
            context = {
                'full_name': f'{self.first_name} {self.last_name}',
                'login_id': self.labor_id,
                'passcode': self.password
            }

            html_message = render_to_string('mail-templates\lobor-login-credentials.html', context)
            plain_message = strip_tags(html_message)



            send_mail(subject, plain_message, from_email, recipient_list)
            self.credential_is_sent = True
        super(labor_register, self).save(*args, **kwargs)