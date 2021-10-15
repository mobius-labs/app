from django.test import TestCase
from apps.account.models import User
# Create your tests here.


class AccountManagerTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email='shiv@gmail.com', password='foo')
        self.assertEqual(user.email, 'shiv@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='supershiv@gmail.com', password='foo')
        self.assertEqual(admin_user.email, 'supershiv@gmail.com')
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='', password='foo')

    def test_str(self):
        user = User.objects.create_user(email='shiv@gmail.com', password='foo')
        string = user.__str__()
        self.assertEqual(string, user.email)

    def test_has_perm(self):
        user = User.objects.create_user(email='shiv@gmail.com', password='foo')
        new_bool = user.has_perm('x')
        self.assertEqual(new_bool, True)

    def test_has_module_perms(self):
        user = User.objects.create_user(email='shiv@gmail.com', password='foo')
        new_bool = user.has_module_perms('x')
        self.assertEqual(new_bool, True)








