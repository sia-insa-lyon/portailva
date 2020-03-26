import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from portailva.association.models import Association, Category
from portailva.directory.api_v1.serializers import DetailDirectoryEntrySerializer
from portailva.directory.models import DirectoryEntry
from portailva.event.models import Event, EventType
from portailva.utils.models import Place


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
                                       category_id=self.category.id,
                                       logo_url="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
                                       room=None)
        self.association.save()

        self.directory = DirectoryEntry(description='descriptionTest',
                                        contact_address='adresse@test.com',
                                        association_id=self.association.id)
        self.directory.save()

        self.place = Place(name="placeName", lat=10.0, long=20.0, is_room=True)
        self.place.save()

        self.eventType = EventType(name="eventTypeName")
        self.eventType.save()

        self.event = Event(name="eventTest",
                           short_description='eventShortDescriptionTest',
                           description='eventDescriptionTest',
                           is_online=True,
                           type=self.eventType,
                           place=self.place,
                           association_id=self.association.id,
                           begins_at=datetime.datetime.now(),
                           ends_at=datetime.datetime.now(),)
        self.event.save()

    def test_model_can_retrieve_a_directory(self):
        """Test the directory model can get a directory."""
        response = self.client.get(
            reverse('api-v1-directory-detail', kwargs={'association_pk': self.association.id}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = DetailDirectoryEntrySerializer(self.directory)
        self.assertEqual(response.data, serializer.data)

    def test_model_can_fail_to_retrieve_a_directory(self):
        """Test the directory model cannot get a directory that doesn't exist."""
        response = self.client.get(reverse('api-v1-directory-detail', kwargs={'association_pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)