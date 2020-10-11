from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    # set up method that is run once before all the tests
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().user_manager.create_superuser(email='admin@gmail.com', password='password')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().user_manager.create_user(email='user@gmail.com', password='password', name='Test User')

    def test_users_listed(self):
        """Tests whenever the users are listed in the Django admin user page"""
        url = reverse('admin:core_user_changelist')
        # IMPORTANT: will use the test client to perform the HTTP GET on the url
        response = self.client.get(url)

        # assertContains - a Django custom assertion that checks that the response
        # contains a certain item
        # checks that the HTTP response was HTTP 200
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # reverse will create the following url: /admin/core/user/1
        response = self.client.get(url)
        # HTTP response code 200 means the response was "OK"
        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

