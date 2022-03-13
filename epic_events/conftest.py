import pytest

USER_ADMIN = 'Alice'
PASS_ADMIN = 'Alice123456'

USER = 'Bob'
PASS_USER = 'Bob123456'


@pytest.fixture()
def admin_user():
    user = {
        'username': USER_ADMIN,
        'password': PASS_ADMIN,
        'team': 'Gestion',
        'is_admin': True
    }
    return user


@pytest.fixture()
def user_support():
    user = {'username': USER, 'password': PASS_USER, 'team': 'Support'}
    return user
