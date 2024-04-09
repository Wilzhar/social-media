
from django.test import TestCase, Client
from factories import UserFactory
from django.urls import reverse


class AuthenticationTestCase(TestCase):
    def test_login_success(self):
        user = UserFactory()
        client = Client()

        response = client.post(
            reverse('login'), {'username': user.username, 'password': 'password'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        client.logout()

    def test_login_failure(self):
        user = UserFactory(password="johnpassword")
        client = Client()

        response = client.post(
            reverse('login'), {'username': user.username, 'password': 'anothepassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        client.logout()

    def test_registration_success(self):
        client = Client()
        username = "jhon245"
        password = "Illicitly5-Salvaging-Sternness"
        email = "jhon245@example.com"

        response = client.post(reverse('register'), {
                               'username': username, 'email': email, 'password1': password, 'password2': password})
        self.assertRedirects(response, reverse('login'), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        client.logout()

    def test_registration_password_mismatch(self):
        client = Client()
        username = "jhon245"
        password1 = "Illicitly5-Salvaging-Sternness"
        password2 = "Native-Unkind-Suspect2"
        email = "jhon245@example.com"

        response = client.post(reverse('register'), {
                               'username': username, 'email': email, 'password1': password1, 'password2': password2})
        self.assertContains(
            response, "The two password fields didn’t match.", status_code=200)

        client.logout()
