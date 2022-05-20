from django.contrib.auth import get_user_model
from django.test import TestCase

from .views import choose


class AdminPagesMiddlewareTestCase(TestCase):
    def test_throws_404_for_anonymous_users(self):
        r = self.client.get("/nora/admin/", follow=True)
        assert r.status_code == 404

    def test_throws_404_for_users(self):
        get_user_model().objects.create_user(
            "ko", "ko@test.com", "pass", is_superuser=False
        )
        self.client.login(username="ko", password="pass")
        r = self.client.get("/nora/admin/", follow=True)
        assert r.status_code == 404

    def test_accessible_for_superusers(self):
        get_user_model().objects.create_user(
            "ko", "ko@test.com", "pass", is_superuser=True
        )
        self.client.login(username="ko", password="pass")
        r = self.client.get("/nora/admin/", follow=True)
        assert r.status_code == 200

    def test_past_hours(self):
        test = choose(self, "ab6ae5ce-f962-4e02-be9b-a755bd13c709")
        self.assertEqual(test, "no existe")
