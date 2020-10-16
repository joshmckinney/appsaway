from django.test import TestCase
from django.contrib.auth.models import User
import datetime

from backend.models import Company, ContractApplication, FreelanceApplication, PermanentApplication


# Test Company Model
class CompanyModelTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Test User")
        self.user = User.objects.get(username="Test User")

    def test_create_company(self):
        self.company = Company.objects.create(
            user=self.user,
            company_name="Test Company",
            company_notes="This is a note",
            contact_name="Test Contact",
            contact_phone="(555) 123-4567",
            contact_email="test@testcompany.com"
        )
        self.assertTrue(Company.objects.get(company_id=1))


# Test Application Models
class AppModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="Test User")

    def setUp(self):
        self.company = Company.objects.create(
            user=self.user,
            company_name="Test Company",
            company_notes="This is a note",
            contact_name="Test Contact",
            contact_phone="(555) 123-4567",
            contact_email="test@testcompany.com"
        )

    def test_create_contract_app(self):
        ContractApplication.objects.create(
            user=self.user,
            company=self.company,
            app_job_title="Test Contract",
            app_date=datetime.date.today(),
            followup_date=datetime.date.today(),
            interview_date=datetime.date.today(),
            app_notes="This is a note",
            status="In Progress",
            contract_start=datetime.date.today(),
            contract_end=datetime.date.today()
        )
        self.assertTrue(ContractApplication.objects.get(app_id=1))

    def test_create_freelance_app(self):
        FreelanceApplication.objects.create(
            user=self.user,
            company=self.company,
            app_job_title="Test Freelance",
            app_date=datetime.date.today(),
            followup_date=datetime.date.today(),
            interview_date=datetime.date.today(),
            app_notes="This is a note",
            status="In Progress",
            freelance_details="Make a website",
            freelance_bid=100.00
        )
        self.assertTrue(FreelanceApplication.objects.get(app_id=1))

    def test_create_permanent_app(self):
        PermanentApplication.objects.create(
            user=self.user,
            company=self.company,
            app_job_title="Test Freelance",
            app_date=datetime.date.today(),
            followup_date=datetime.date.today(),
            interview_date=datetime.date.today(),
            app_notes="This is a note",
            status="In Progress"
        )
        self.assertTrue(PermanentApplication.objects.get(app_id=1))
