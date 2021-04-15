import json

from rest_framework.test import APITestCase, APIClient

from authentication.models import User

from .models import Profile

class ProfileNotLoginedTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'testtest')
    
    def test_get_profile(self):
        response = self.client.get('/api/profiles/test/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['username'], 'test')
        self.assertEqual(response_jsonified['email'], 'test@test.com')
        self.assertEqual(response_jsonified['profile']['bio'], '')
    
    def test_change_profile(self):
        response = self.client.put('/api/profiles/test/', {'user': {'username': 'test-changed', 'profile': {'bio': 'testbio'}}})
        
        self.assertEqual(response.status_code, 401)

class ProfileLoginedTetsCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)
    
    def test_get_profile(self):
        response = self.client.get('/api/profiles/test/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['username'], 'test')
        self.assertEqual(response_jsonified['email'], 'test@test.com')
        self.assertEqual(response_jsonified['profile']['bio'], '')
    
    def test_change_profile(self):
        response = self.client.put('/api/profiles/test/', {'user': {'username': 'test-changed', 'profile': {'bio': 'testbio'}}})
        
        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['username'], 'test-changed')
        self.assertEqual(response_jsonified['profile']['bio'], 'testbio')
    
    def test_change_profile_without_specified_username(self):
        response = self.client.put('/api/profiles/', {'user': {'username': 'test-changed', 'profile': {'bio': 'testbio'}}})
        
        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['username'], 'test-changed')
        self.assertEqual(response_jsonified['profile']['bio'], 'testbio')
    
    def test_change_other_user_profile(self):
        other_user = User.objects.create_user('test-other', 'test-other@test.com', 'testtesttest')

        response = self.client.put('/api/profiles/test-other/', {'user': {'username': 'test-changed', 'profile': {'bio': 'testbio'}}})

        self.assertEqual(response.status_code, 403)
