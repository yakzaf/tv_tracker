from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from tracker.models import Show
from tracker.serializers import ShowSerializer
from django.db.models import Q

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def new_show_items(show, overview, kind, year, service):
        if show != '' and overview != '' and kind != '' and year != '' and service != []:
            Show.objects.create(show_name=show, overview=overview,
                                kind=kind, year=year, service=service)

    def setUp(self):
        # add test data
        self.new_show_items('Test1', 'Lorem ipsum dolor sit amet',
                            kind='Series', year='1999', service=["Netflix", "iTunes"])
        self.new_show_items('Test2', 'consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolor',
                            kind='Movie', year='2004', service=[])
        self.new_show_items('Test3', 'Ut enim ad minim veniam',
                            kind='Movie', year='1993', service=["Amazon Prime Video"])
        self.new_show_items('Test4', 'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequa',
                            kind='Series', year='2012-2014', service=["Disney+"])
        self.new_show_items('Test5', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu',
                            kind='Series', year='2020-', service=["Google Play"])


class GetAllItemsTest(BaseViewTest):

    def test_get_all_items(self):
        """
        This test ensures that all items added in the setUp method
        exist when we make a GET request to the hm/ endpoint
        """
        # hit the api endpoint
        response = self.client.get(reverse("api-search"), {"name": "Test"})
        # fetch the data from db
        expected = Show.objects.all()
        serialized = ShowSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_item(self):
        """
        This test checks the parameters
        """
        # hit the api endpoint with parameters
        response = self.client.get(reverse("api-search"), {"name": "Test1"})
        # fetch the only item matching the name
        expected = Show.objects.filter(Q(show_name__icontains="Test1"))
        serialized = ShowSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
