from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CustomUserModelTests(TestCase):
    def test_age_is_computed_from_birthday(self):
        user = get_user_model()(username="kim", birthday=date(2000, 1, 1))
        today = date.today()
        expected = today.year - 2000 - ((today.month, today.day) < (1, 1))
        self.assertEqual(user.age, expected)

    def test_age_is_none_without_birthday(self):
        user = get_user_model()(username="kim")
        self.assertIsNone(user.age)


class SignUpViewTests(TestCase):
    def test_signup_page_renders(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_fields_use_bootstrap_widgets(self):
        response = self.client.get(reverse("signup"))
        self.assertContains(response, 'type="date"')
        self.assertContains(response, 'class="form-select"')
        self.assertContains(response, 'class="form-control"')

    def test_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "student1",
                "first_name": "Juan",
                "last_name": "Dela Cruz",
                "gender": "Cisgender Male",
                "contact_number": "09171234567",
                "email": "juan@example.com",
                "school": "University of the Philippines",
                "degree_program": "BS Computer Science",
                "password1": "a-Strong-pass-123",
                "password2": "a-Strong-pass-123",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Your account is ready.")
        self.assertTrue(get_user_model().objects.filter(username="student1").exists())

    def test_signup_rejects_duplicate_email(self):
        get_user_model().objects.create_user(username="existing", email="juan@example.com", password="x")
        response = self.client.post(
            reverse("signup"),
            {
                "username": "student1",
                "email": "juan@example.com",
                "password1": "a-Strong-pass-123",
                "password2": "a-Strong-pass-123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fix the highlighted fields below.")
        self.assertFalse(get_user_model().objects.filter(username="student1").exists())


class LoginViewTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(username="student1", email="juan@example.com", password="a-Strong-pass-123")

    def test_login_page_renders_styled_form(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertContains(response, 'class="form-control"')

    def test_login_with_wrong_password_shows_error(self):
        response = self.client.post(reverse("login"), {"username": "student1", "password": "wrong"})
        self.assertContains(response, "alert-danger")

    def test_logged_in_user_is_redirected_away_from_login(self):
        self.client.login(username="student1", password="a-Strong-pass-123")
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("home"))
