from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
import sys
from .models import Poll
from datetime import datetime

# Create your tests here.
class SearchTestCase(TestCase):
    #sys.stderr.write(users['users'][0]['label'])
    def setUp(self):
        self.username = "UnitTestUser"
        user = User.objects.create_user(self.username, "romain@gmail.com", "test")

        self.poll_name = "UnitTestPoll"
        self.poll_desc = "UnitTestPollDesc"

        Poll.objects.create(name=self.poll_name, 
        owner=user, 
        is_private=False,
        description=self.poll_desc,
        expiration_date=datetime.now())

        self.client = Client()

    def test_users_search(self):
        users = self.client.get(f"/searchUsers/{self.username}").json()
        
        username = users['users'][0]['label']
        self.assertTrue(username, self.username)

    def test_polls_search(self):
        polls = self.client.get("/searchPolls/UnitTestPoll").json()

        poll_name = polls['polls'][0]['name']
        poll_desc = polls['polls'][0]['description']

        self.assertTrue(poll_name, self.poll_name)
        self.assertTrue(poll_desc, self.poll_desc)

class GetPageTestCase(TestCase):
    def setUp(self):
        
        self.client = Client()
        self.code_OK = 200

    def test_home(self):
        response = self.client.get('')

        self.assertTrue(response.status_code, self.code_OK)

    def test_create_poll_form(self):
        response = self.client.get('/createPollForm')

        self.assertTrue(response.status_code, self.code_OK)

    def test_resgister(self):
        response = self.client.get('/register')

        self.assertTrue(response.status_code, self.code_OK)

    def test_login(self):
        response = self.client.get('/accounts/login')

        self.assertTrue(response.status_code, self.code_OK)