from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CustomSignupForm, EditProfileForm

User = get_user_model()

class AccountsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='Password123!',
            role='buyer',
            nickname='testuser',
            phone_number='+821012341234',
            is_agree_terms=True,
            is_agree_privacy_policy=True,
        )

    def test_signup_view(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

        form_data = {
            'email': 'newuser@example.com',
            'password1': 'NewPassword123!',
            'password2': 'NewPassword123!',
            'nickname': 'newuser',
            'phone_number': '+821012341235',  # Changed to a different phone number
            'is_agree_terms': True,
            'is_agree_privacy_policy': True,
            'role': 'buyer',  # Ensure role is included
        }
        response = self.client.post(reverse('account_signup'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_view(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        login_data = {
            'login': 'testuser@example.com',
            'password': 'Password123!',
        }
        response = self.client.post(reverse('account_login'), login_data)
        self.assertEqual(response.status_code, 302)

    def test_mypage_view(self):
        self.client.login(email='testuser@example.com', password='Password123!')
        response = self.client.get(reverse('mypage_nav'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/mypage_nav.html')

    def test_edit_profile_view(self):
        self.client.login(email='testuser@example.com', password='Password123!')
        response = self.client.get(reverse('mypage_section', args=['edit_profile']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

        edit_data = {
            'nickname': 'updateduser',
            'phone_number': '+821012341235',
            'email': 'testuser@example.com',
            'is_agree_terms': True,
            'is_agree_privacy_policy': True,
        }
        response = self.client.post(reverse('mypage_section', args=['edit_profile']), edit_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, 'updateduser')
        self.assertEqual(self.user.phone_number, '+821012341235')

    def test_custom_signup_form_validation(self):
        form_data = {
            'email': 'newuser@example.com',
            'password1': 'NewPassword123!',
            'password2': 'NewPassword123!',
            'nickname': 'newuser',
            'phone_number': '+821012341235',
            'is_agree_terms': True,
            'is_agree_privacy_policy': True,
            'role': 'buyer',  # Ensure role is included
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_profile_form_validation(self):
        form_data = {
            'nickname': 'updateduser',
            'phone_number': '+821012341235',
            'email': 'testuser@example.com',
            'is_agree_terms': True,
            'is_agree_privacy_policy': True,
        }
        form = EditProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, 'updateduser')
        self.assertEqual(self.user.phone_number, '+821012341235')
