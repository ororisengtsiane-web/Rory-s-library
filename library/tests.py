from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

class Chapter4RoleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('setup_roles', verbosity=0)
        cls.member = User.objects.create_user('member_test', password='SecurePass!2026')
        cls.member.groups.add(Group.objects.get(name='Member'))
        cls.librarian = User.objects.create_user('librarian_test', password='SecurePass!2026')
        cls.librarian.groups.add(Group.objects.get(name='Librarian'))

    def test_anonymous_add_book_redirects_to_login(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_member_cannot_add_book(self):
        self.client.force_login(self.member)
        self.assertEqual(self.client.get(reverse('add_book')).status_code, 403)

    def test_librarian_can_add_book(self):
        self.client.force_login(self.librarian)
        self.assertEqual(self.client.get(reverse('add_book')).status_code, 200)

    def test_registration_assigns_member(self):
        response = self.client.post(reverse('register'), {
            'username':'new_member', 'email':'new_member@example.com',
            'password1':'SecurePass!2026', 'password2':'SecurePass!2026'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(username='new_member').groups.filter(name='Member').exists())

    def test_profile_requires_login(self):
        self.assertEqual(self.client.get(reverse('profile')).status_code, 302)

    def test_member_cannot_toggle_availability(self):
        self.client.force_login(self.member)
        self.assertEqual(self.client.post('/books/1/toggle-availability/').status_code, 403)
