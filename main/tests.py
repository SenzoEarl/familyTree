from django.test import TestCase
from django.urls import reverse
from .models import FamilyMember
from django.contrib.auth import get_user_model

class FamilyMemberTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')

    def test_create_family_member(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('familyTree:family_member_create'), {
            'name': 'John Doe',
            'gender': 'Male',
            'birth_date': '1980-01-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FamilyMember.objects.filter(name='John Doe').exists())
