from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from portailva.association.models import Association, Category
from portailva.directory.api_v1.serializers import DirectoryEntrySerializer
from portailva.directory.models import DirectoryEntry


class DirectoryTestCase(TestCase):
    """This class defines the test suite for the directory model API route."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        self.category = Category(name='categorieTest',
                                 position=1,
                                 latex_color_name='red')
        self.category.save()

        self.association = Association(name='assoTest',
                                       description='courteDescriptionTest',
                                       category_id=self.category.id)
        self.association.save()

        self.directory = DirectoryEntry(description='descriptionTest',
                                        contact_address='adresse@test.com',
                                        association_id=self.association.id)
        self.directory.save()

    def test_model_can_retrieve_a_directory(self):
        """Test the directory model can get a directory."""
        response = self.client.get(
            reverse('api-v1-directory-public', kwargs={'association_pk': self.association.id}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = DirectoryEntrySerializer(self.directory)
        self.assertEqual(response.data, serializer.data)

    def test_model_can_fail_to_retrieve_a_directory(self):
        """Test the directory model cannot get a directory that doesn't exist."""
        response = self.client.get(reverse('api-v1-directory-public', kwargs={'association_pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)