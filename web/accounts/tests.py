# accounts/tests/test_accounts.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import UserRegistrationHistory

class AccountsTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='testuser@example.com',
            password='ComplexPass123!',
            role='buyer',
            nickname='testuser',
            phone_number='1234567890',
            is_agree_terms=True,
            is_agree_privacy_policy=True
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.nickname, 'testuser')
        self.assertTrue(self.user.check_password('ComplexPass123!'))
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertTrue(self.user.is_agree_terms)
        self.assertTrue(self.user.is_agree_privacy_policy)

    def test_user_login(self):
        login = self.client.login(email='testuser@example.com', password='ComplexPass123!')
        self.assertTrue(login)

    def test_user_registration_history(self):
        registration_history = UserRegistrationHistory.objects.create(user=self.user)
        self.assertEqual(registration_history.user.email, 'testuser@example.com')
        self.assertIsNotNone(registration_history.registration_date)
        self.assertIsNone(registration_history.withdrawal_date)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_custom_signup_form(self):
        response = self.client.post(reverse('account_signup'), {
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'nickname': 'newuser',
            'phone_number': '0987654321',
            'is_agree_terms': True,
            'is_agree_privacy_policy': True
        })
        if response.status_code != 302:
            print(response.content)  # 응답 내용을 출력하여 오류 메시지를 확인
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        new_user = self.User.objects.get(email='newuser@example.com')
        self.assertEqual(new_user.nickname, 'newuser')
        self.assertEqual(new_user.phone_number, '0987654321')
        self.assertTrue(new_user.is_agree_terms)
        self.assertTrue(new_user.is_agree_privacy_policy)
