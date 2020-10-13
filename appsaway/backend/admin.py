from django.contrib import admin

# Register your models here.
from .models import Company, ContractApplication, PermanentApplication, FreelanceApplication

admin.site.register(Company)
admin.site.register(ContractApplication)
admin.site.register(PermanentApplication)
admin.site.register(FreelanceApplication)
