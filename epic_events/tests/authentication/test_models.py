import pytest

from authentication.models import User


class TestUserManager:
    """
    Class to test user creation

    Methods
    -------
    test_create_user(self):
        creates user with valid arguments
        check data
    test_create_superuser(self):
        creates user with valid arguments
        check data
    """

    @pytest.mark.django_db
    def test_create_user(self, user_support):
        user = User.objects.create(**user_support)

        expected_value = user_support['username']

        assert str(user) == expected_value

        user = User.objects.get(username=user_support['username'])
        assert user.team == 'Support'
        assert user.is_admin is False

    @pytest.mark.django_db
    def test_create_superuser(self, admin_user):
        user = User.objects.create(**admin_user)

        expected_value = admin_user['username']

        assert str(user) == expected_value

        user = User.objects.get(username=admin_user['username'])
        assert user.team == 'Gestion'
        assert user.is_admin is True
