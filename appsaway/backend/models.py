from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel


# Company Model
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, null=False)
    company_notes = models.CharField(max_length=200, null=True)
    contact_name = models.CharField(max_length=200, null=True)
    contact_email = models.CharField(max_length=100, null=True)
    contact_phone = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name


# Application Model
class Application(PolymorphicModel):
    app_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_job_title = models.CharField(max_length=200, null=False, verbose_name='Job Title')
    app_date = models.DateField(auto_now=False, auto_now_add=False, null=False, verbose_name='App Date')
    interview_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name='Interview Date')
    followup_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name='Follow-up Date'
    )
    last_updated = models.DateTimeField(auto_now_add=True, verbose_name='Last Updated')
    app_notes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Notes')
    status = models.CharField(max_length=20, verbose_name='Status', choices=[
        ('In Progress', 'In Progress'),
        ('Submitted', 'Submitted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected')
    ])

    def __str__(self):
        return self.app_job_title + \
               ' (' + self.company.company_name + ')'


# Contract Application Model
class ContractApplication(Application):
    contract_start = models.DateField(auto_now=False, auto_now_add=False, null=False, verbose_name='Contract Start')
    contract_end = models.DateField(auto_now=False, auto_now_add=False, null=False, verbose_name='Contract End')


# Permanent Application Model
class PermanentApplication(Application):
    pass


# Freelance Application Model
class FreelanceApplication(Application):
    freelance_details = models.CharField(max_length=200, null=False, verbose_name='Job Details')
    freelance_bid = models.FloatField(null=False, verbose_name='Bid Amount')
