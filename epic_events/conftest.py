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


@pytest.fixture()
def client_test():
    client = {'name': 'Client_Test', 'email': 'test@test.local', 'last_name': 'Dupond'}
    return client


@pytest.fixture()
def contract_test():
    contract = {'amount': '7123.13', 'payment_due': '2022-03-17', 'client_id': 'Client_Test'}
    return contract


@pytest.fixture()
def event_test():
    event = {'attendees': '153', 'event_date': '2022-03-20', 'notes': 'test event'}
    return event
