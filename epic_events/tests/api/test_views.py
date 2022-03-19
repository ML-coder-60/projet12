from django.test import TestCase, Client
from authentication.models import User
import json


class TestClients(TestCase):
    """
    Class to test View Clients

    Methods
    -------
    create client :
        test_create_client_team_support()
        test_create_client_no_user()
        test_create_client_team_sales()

    update client :

        test_update_client_team_support()
        test_create_client_no_user()
        test_create_client_user_sales_not_owner()
        test_create_client_user_sales_owner()

    test_clients_list(self):
        check data with user sales
        check data with filter user support
        check data with search user admin
        check data with user no authenticated

    test_login_user(self):
        check views admin interface  redirect (302) with user
    """

    CLIENT = {
        'name': 'Company',
        'last_name': 'Bob',
        'first_name': 'dupond',
        'email': 'test@test.local',
        'phone': '123456789',
        'mobile': '987654321',
        'confirmed': False
    }

    CLIENT_TEST = {
        'name': 'Company_test',
        'last_name': 'Bob',
        'first_name': 'dupond',
        'email': 'test2@test.local',
        'phone': '123456789',
        'mobile': '987654321',
        'confirmed': True
    }

    def setUp(self):
        self.token_sales = self.get_token_user(team='Commercial')
        self.token_support = self.get_token_user(team='Support')

    def create_user(self, team):
        self.username = User.objects.make_random_password()
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = False
        user.is_active = True
        user.team = team
        user.save()

    def create_client(self):
        url = '/clients/'
        client = Client()
        resp = client.post(
            url,
            data=json.dumps(self.CLIENT),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token_sales}'}
        )
        return resp.json()

    def get_token_user(self, team):
        self.create_user(team)
        url = '/login/'
        client = Client()
        resp = client.post(url, {'username': self.username, 'password': self.password})
        return resp.data['access']

    def test_create_client_team_support(self):
        url = '/clients/'
        client = Client()
        resp = client.post(
            url,
            data=json.dumps(self.CLIENT),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token_support}'}
        )
        assert resp.status_code == 403
        assert "Vous n'avez pas la permission d'effectuer cette action." in resp.content.decode()

    def test_create_client_no_user(self):
        url = '/clients/'
        client = Client()
        resp = client.post(
            url,
            data=json.dumps(self.CLIENT),
            content_type='application/json'
        )
        assert resp.status_code == 401
        assert "Informations d\'authentification non fournies." in resp.content.decode()

    def test_create_client_team_sales(self):
        url = '/clients/'
        client = Client()
        resp = client.post(
            url,
            data=json.dumps(self.CLIENT_TEST),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token_sales}'}
        )
        assert resp.status_code == 201
        assert resp.data['name'] == self.CLIENT_TEST['name']
        assert resp.data['last_name'] == self.CLIENT_TEST['last_name']
        assert resp.data['first_name'] == self.CLIENT_TEST['first_name']
        assert resp.data['email'] == self.CLIENT_TEST['email']
        assert resp.data['phone'] == self.CLIENT_TEST['phone']
        assert resp.data['mobile'] == self.CLIENT_TEST['mobile']
        assert resp.data['confirmed'] == self.CLIENT_TEST['confirmed']

    def test_list_clients_no_authenticated(self):
        url = '/clients/'
        client = Client()
        resp = client.get(url)

        assert resp.status_code == 401
        assert "Informations d\'authentification non fournies." in resp.content.decode()

    def test_list_clients_team_sales(self):
        self.create_client()
        url = '/clients/'
        client = Client()
        resp = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {self.token_sales}'})

        assert resp.status_code == 200
        result = resp.json()
        assert 1 == result['count']
        assert self.CLIENT['email'] == result['results'][0]['email']
        assert self.CLIENT['first_name'] == result['results'][0]['first_name']
        assert self.CLIENT['last_name'] == result['results'][0]['last_name']
        assert self.CLIENT['confirmed'] == result['results'][0]['confirmed']
        assert self.CLIENT['phone'] == result['results'][0]['phone']
        assert self.CLIENT['mobile'] == result['results'][0]['mobile']

    def test_list_clients_team_support(self):
        """
            Client not confirmed is not display for team Support
        """
        self.create_client()
        url = '/clients/'
        client = Client()
        resp = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {self.token_support}'})

        assert resp.status_code == 404
        assert "Pas trouvé." in resp.content.decode()

    def test_update_client_no_user(self):
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.put(
            url,
            data=json.dumps(self.CLIENT),
            content_type='application/json'
        )
        assert resp.status_code == 401
        assert "Informations d\'authentification non fournies." in resp.content.decode()

    def test_update_client_team_support(self):
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.put(
            url,
            data=json.dumps(self.CLIENT),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token_support}'}
        )
        assert resp.status_code == 403
        assert "Vous n'avez pas la permission d'effectuer cette action." in resp.content.decode()

    def test_update_client_team_sale_no_owner(self):
        token = self.get_token_user(team='Commercial')
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.put(
             url,
             data=json.dumps(self.CLIENT),
             content_type='application/json',
             **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        assert resp.status_code == 403
        assert "Vous n'avez pas la permission d'effectuer cette action." in resp.content.decode()

    def test_update_client_team_sale_owner(self):
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.put(
             url,
             data=json.dumps(self.CLIENT),
             content_type='application/json',
             **{'HTTP_AUTHORIZATION': f'Bearer {self.token_sales}'}
        )
        assert resp.status_code == 200
        assert resp.data['name'] == self.CLIENT['name']
        assert resp.data['last_name'] == self.CLIENT['last_name']
        assert resp.data['first_name'] == self.CLIENT['first_name']
        assert resp.data['email'] == self.CLIENT['email']
        assert resp.data['phone'] == self.CLIENT['phone']
        assert resp.data['mobile'] == self.CLIENT['mobile']
        assert resp.data['confirmed'] == self.CLIENT['confirmed']

    def test_detail_client_no_user(self):
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.get(url)
        assert resp.status_code == 401
        assert "Informations d\'authentification non fournies." in resp.content.decode()

    def test_detail_client_team_support(self):
        """
             Client not confirmed is not display for team Support
        """
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {self.token_support}'})
        assert resp.status_code == 404
        assert "Pas trouvé." in resp.content.decode()

    def test_detail_client_team_sale_no_owner(self):
        token = self.get_token_user(team='Commercial')
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.put(
             url,
             data=json.dumps(self.CLIENT),
             content_type='application/json',
             **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        assert resp.status_code == 403
        assert "Vous n'avez pas la permission d'effectuer cette action." in resp.content.decode()

    def test_detail_client_team_sale_owner(self):
        data_client = self.create_client()
        id_client = data_client['id']
        url = f'/clients/{id_client}/'
        client = Client()
        resp = client.put(
             url,
             data=json.dumps(self.CLIENT),
             content_type='application/json',
             **{'HTTP_AUTHORIZATION': f'Bearer {self.token_sales}'}
        )

        assert resp.status_code == 200
        assert resp.data['name'] == self.CLIENT['name']
        assert resp.data['last_name'] == self.CLIENT['last_name']
        assert resp.data['first_name'] == self.CLIENT['first_name']
        assert resp.data['email'] == self.CLIENT['email']
        assert resp.data['phone'] == self.CLIENT['phone']
        assert resp.data['mobile'] == self.CLIENT['mobile']
        assert resp.data['confirmed'] == self.CLIENT['confirmed']
