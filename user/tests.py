from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class UserTest(TestCase):

    # user creation test.
    def test_user_creation(self):
        user = User.objects.create_user(
            email='test@gmail.com',
            username='test',
            first_name ='test',
            last_name ='t',
            password='test123'
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 't')
        self.assertTrue(user.check_password('test123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    # super_user creation test.
    def test_superuser_creation(self):

        admin_user = User.objects.create_superuser(
            email='test_admin@gmail.com',
            username='test_admin',
            first_name='test_admin',
            last_name='t',
            password='test_admin123'
        )
        self.assertEqual(admin_user.email, 'test_admin@gmail.com')
        self.assertEqual(admin_user.username, 'test_admin')
        self.assertEqual(admin_user.first_name, 'test_admin')
        self.assertEqual(admin_user.last_name, 't')
        self.assertTrue(admin_user.check_password('test_admin123'))
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
