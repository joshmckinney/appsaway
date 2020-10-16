import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from backend.models import Company
from backend.forms import Company as CompanyForm
from backend.forms import ContractApplication as ContractForm
from backend.forms import FreelanceApplication as FreelanceForm
from backend.forms import PermanentApplication as PermanentForm


class TestCompanyForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Test User", password="Password")

    def test_company_form(self):
        form_data = {
            "company_name": "Test Company",
            "company_notes": "Some notes",
            "contact_name": "Some Contact",
            "contact_phone": "(555) 123-4567",
            "contact_email": "test@testcompany.com",
            "user": self.user
        }
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestContractApplicationForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Test User", password="Password")
        self.company = Company.objects.create(company_name="Test Company", user=self.user)

    def test_contract_form(self):
        form_data = {
            "company": self.company.pk,
            "user": self.user.pk,
            "app_job_title": "Test Job",
            "app_date": datetime.date.today(),
            "followup_date": datetime.date.today(),
            "interview_date": datetime.date.today(),
            "app_notes": "Some job notes",
            "status": "Hired",
            "contract_start": datetime.date.today(),
            "contract_end": datetime.date.today()
        }
        form = ContractForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestFreelanceApplicationForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Test User", password="Password")
        self.company = Company.objects.create(company_name="Test Company", user=self.user)

    def test_freelance_form(self):
        form_data = {
            "company": self.company.pk,
            "user": self.user.pk,
            "app_job_title": "Test Job",
            "app_date": datetime.date.today(),
            "followup_date": datetime.date.today(),
            "interview_date": datetime.date.today(),
            "app_notes": "Some job notes",
            "status": "Hired",
            "freelance_details": "Another Gig",
            "freelance_bid": 25.00
        }
        form = FreelanceForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestPermanentApplicationForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Test User", password="Password")
        self.company = Company.objects.create(company_name="Test Company", user=self.user)

    def test_freelance_form(self):
        form_data = {
            "company": self.company.pk,
            "user": self.user.pk,
            "app_job_title": "Test Job",
            "app_date": datetime.date.today(),
            "followup_date": datetime.date.today(),
            "interview_date": datetime.date.today(),
            "app_notes": "Some job notes",
            "status": "Hired"
        }
        form = PermanentForm(data=form_data)
        self.assertTrue(form.is_valid())
