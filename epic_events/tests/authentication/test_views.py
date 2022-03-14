from django.test import TestCase, Client
from authentication.models import User


class TestAdminPanel(TestCase):
    """
    Class to test login admin interface and view models

    Methods
    -------
    test_login_admin(self):
        check views admin interface with user admin
    test_login_user(self):
        check views admin interface  redirect (302) with user
    """

    URL = [
            '/gestion/',
            '/gestion/authentication/user/',
            '/gestion/authentication/user/add/',
            '/gestion/password_change/',
            '/gestion/authentication/user/?team__exact=Support',
            '/gestion/authentication/user/?is_active__exact=0&team__exact=Gestion',
            '/gestion/authentication/user/?is_active__exact=1&team__exact=Vente',
            '/gestion/logout/'
        ]

    def create_user(self, admin=False):
        self.username = User.objects.make_random_password()
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = admin
        user.is_superuser = admin
        user.is_active = True
        user.save()

    def test_login_admin_views(self):
        self.create_user(admin=True)
        client = Client()
        client.login(username=self.username, password=self.password)

        for url in self.URL:
            resp = client.get(url)
            print(url, resp.status_code)
            assert resp.status_code == 200
            assert "<!DOCTYPE html" in resp.content.decode()

    def test_login_user_views(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)

        for url in self.URL:
            resp = client.get(url)
            # print(url, resp.status_code)
            assert resp.status_code == 302


class TestLoginToken(TestCase):
    """
    Class to test login and get Token for API

    Methods
    -------
    test_login_admin(self):
        check views admin interface with user admin
    test_login_user(self):
        check views admin interface  redirect (302) with user

    """

    def create_user(self, admin=False):
        self.username = User.objects.make_random_password()
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = admin
        user.is_superuser = admin
        user.is_active = True
        user.save()

    def test_login_user_token(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)

        url = '/login/'
        resp = client.post(url, {'username': self.username, 'password': self.password})
        assert resp.status_code == 200

    def test_login_super_user_token(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)

        url = '/login/'
        resp = client.post(url, {'username': self.username, 'password': self.password})
        assert resp.status_code == 200

    def test_login_user_pass_ko(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)

        url = '/login/'
        resp = client.post(url, {'username': self.username, 'password': 'mdp'})
        assert resp.status_code == 401

    def test_change_password_password_ko(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)

        url = '/login/'
        resp = client.post(url, {'username': self.username, 'password': 'mdp'})
        assert resp.status_code == 401

    def test_change_password_password_ok(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)

        url = '/login/'
        resp = client.post(url, {'username': self.username, 'password': 'mdp'})
        assert resp.status_code == 401
