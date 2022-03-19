import pytest
from api.models import Client, Contract, Event


class TestClient:
    """
    Class to test client creation

    Methods
    -------
    test_create_client(self):
        creates user with valid arguments
        check data
    """

    @pytest.mark.django_db
    def test_create_client(self, client_test):

        client = Client.objects.create(**client_test)
        client.save()
        expected_value = client_test['name']

        assert str(client) == expected_value

        client = Client.objects.get(last_name=client_test['last_name'])
        assert client.email == client_test['email']
        assert client.confirmed is False
        assert client.first_name == ''
        assert client.phone == ''
        assert client.mobile == ''
        assert client.sales_user is None


class TestContract:
    """
    Class to test contract creation

    Methods
    -------
    Create client_test and
    test_create_contract(self):
        creates contract with valid arguments
        check data
    """

    @pytest.mark.django_db
    def test_create_contract(self, client_test, contract_test):

        client = Client.objects.create(**client_test)
        client.save()

        contract_test['client_id'] = client.id

        contract = Contract.objects.create(**contract_test)
        contract.save()

        expected_value = "1-"+str(client_test['name'])
        assert str(contract) == expected_value

        contract = Contract.objects.get(amount=contract_test['amount'])
        assert contract.signed is False
        assert contract.amount == float(contract_test['amount'])
        assert contract.client_id == client.id


class TestEvent:
    """
     Class to test Event creation

     Methods
     -------
     Create client_test and
     Create contract_test and
     test_create_contract(self):
         creates contract with valid arguments
         check data
     """

    @pytest.mark.django_db
    def test_create_event(self, client_test, contract_test, event_test):

        client = Client.objects.create(**client_test)
        client.save()

        contract_test['client_id'] = client.id

        contract = Contract.objects.create(**contract_test)
        contract.save()

        event_test['contract_id'] = contract.id
        event = Event.objects.create(**event_test)
        event.save()

        event = Event.objects.get(attendees=event_test['attendees'])

        expected_value = contract.id
        assert event.contract_id == expected_value

        assert event.completed is False
        assert event.notes == event_test['notes']
        assert event.support_user_id is None
