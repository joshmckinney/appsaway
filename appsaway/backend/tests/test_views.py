import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from backend.models import PermanentApplication, Company


class PageAuth(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create data for class to persist through all tests
        cls.user = User.objects.create_user(username="Test User", password="Password")
        cls.company = Company.objects.create(
            user=cls.user,
            company_name="Test Company",
            company_notes="This is a note",
            contact_name="Test Contact",
            contact_phone="(555) 123-4567",
            contact_email="test@testcompany.com"
        )
        cls.application = PermanentApplication.objects.create(
            user=cls.user,
            company=cls.company,
            app_job_title="Test Freelance",
            app_date=datetime.date.today(),
            followup_date=datetime.date.today(),
            interview_date=datetime.date.today(),
            app_notes="This is a note",
            status="In Progress"
        )

    def test_anonymous(self):
        # Test anonymous user can't access any private url, gets redirected to /accounts/login/?next={...}
        home = self.client.get(reverse("home"))
        app_view = self.client.get(reverse("app", args=[1]))
        app_list = self.client.get(reverse("applist"))
        app_create = self.client.get(reverse("createapp"))
        app_edit = self.client.get(reverse("editapp", args=[1]))
        app_delete = self.client.get(reverse("deleteapp", args=[1]))
        company_view = self.client.get(reverse("company", args=[1]))
        company_list = self.client.get(reverse("companylist"))
        company_create = self.client.get(reverse("createcompany"))
        company_edit = self.client.get(reverse("editcompany", args=[1]))
        company_delete = self.client.get(reverse("deletecompany", args=[1]))
        profile = self.client.get(reverse("profile"))
        profile_edit = self.client.get(reverse("editprofile"))
        profile_delete = self.client.get(reverse("deleteprofile"))

        # All urls accessed above should be redirected as they are private
        self.assertRedirects(home, "/accounts/login/?next=/dashboard/")
        self.assertRedirects(app_view, "/accounts/login/?next=/app/1")
        self.assertRedirects(app_list, "/accounts/login/?next=/app/list")
        self.assertRedirects(app_create, "/accounts/login/?next=/app/create")
        self.assertRedirects(app_edit, "/accounts/login/?next=/app/edit/1")
        self.assertRedirects(app_delete, "/accounts/login/?next=/app/delete/1")
        self.assertRedirects(company_view, "/accounts/login/?next=/company/1")
        self.assertRedirects(company_list, "/accounts/login/?next=/company/list")
        self.assertRedirects(company_create, "/accounts/login/?next=/company/create")
        self.assertRedirects(company_edit, "/accounts/login/?next=/company/edit/1")
        self.assertRedirects(company_delete, "/accounts/login/?next=/company/delete/1")
        self.assertRedirects(profile, "/accounts/login/?next=/profile/")
        self.assertRedirects(profile_edit, "/accounts/login/?next=/profile/edit")
        self.assertRedirects(profile_delete, "/accounts/login/?next=/profile/delete")

    def test_authenticated(self):
        # User should be able to access private urls associated with them once authenticated
        self.client.force_login(user=self.user)  # Authenticate user
        home = self.client.get(reverse("home"))
        app_view = self.client.get(reverse("app", args=[1]))
        app_list = self.client.get(reverse("applist"))
        app_create = self.client.get(reverse("createapp"))
        app_edit = self.client.get(reverse("editapp", args=[1]))
        app_delete = self.client.get(reverse("deleteapp", args=[1]))
        company_view = self.client.get(reverse("company", args=[1]))
        company_list = self.client.get(reverse("companylist"))
        company_create = self.client.get(reverse("createcompany"))
        company_edit = self.client.get(reverse("editcompany", args=[1]))
        company_delete = self.client.get(reverse("deletecompany", args=[1]))
        profile = self.client.get(reverse("profile"))
        profile_edit = self.client.get(reverse("editprofile"))
        profile_delete = self.client.get(reverse("deleteprofile"))

        # All private urls besides delete should return 200
        self.assertEqual(home.status_code, 200)
        self.assertEqual(app_view.status_code, 200)
        self.assertEqual(app_list.status_code, 200)
        self.assertEqual(app_create.status_code, 200)
        self.assertEqual(app_edit.status_code, 200)
        self.assertEqual(app_delete.status_code, 302)  # App was deleted.. redirected to /app/list/
        self.assertEqual(PermanentApplication.objects.all().count(), 0)  # Confirm app doesn't exist anymore
        self.assertEqual(company_view.status_code, 200)
        self.assertEqual(company_list.status_code, 200)
        self.assertEqual(company_create.status_code, 200)
        self.assertEqual(company_edit.status_code, 200)
        self.assertEqual(company_delete.status_code, 302)  # Company was deleted.. redirected to /company/list/
        self.assertEqual(Company.objects.all().count(), 0)  # Confirm company doesn't exist anymore
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile_edit.status_code, 200)
        self.assertEqual(profile_delete.status_code, 302)  # User was deleted.. redirected to index
        self.assertEqual(User.objects.all().count(), 0)  # Confirm user doesn't exist anymore
