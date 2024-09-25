from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class PersonnageAPITest(APITestCase):
    def test_list_personnages(self):
        url = reverse('personnage-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) #test de l'api 

#testcase de l'api dans le shell