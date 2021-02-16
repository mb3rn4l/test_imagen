import io
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.test import TestCase
from unittest.mock import patch, MagicMock
from unittest import mock

from apps.image_services.models import ImageFile


class ImageTest(TestCase):
    def setUp(self):
        self.image = ImageFile()

    @patch('apps.image_services.models.ImageFile.dimensions', new_callable=mock.PropertyMock)
    def test_is_portrait(self, mock_dimensions):
        mock_dimensions.return_value = (500, 300)
        self.assertEqual(False, self.image.is_portrait())

        mock_dimensions.return_value = (300, 500)
        self.assertEqual(True, self.image.is_portrait())

    @patch('apps.image_services.models.ImageFile.dimensions', new_callable=mock.PropertyMock)
    def test_get_a4_dimensions(self, mock_dimensions):
        mock_dimensions.return_value = (500, 300)
        self.assertEqual(self.image.A4_LANDSCAPE, self.image.get_a4_dimensions())

        mock_dimensions.return_value = (300, 500)
        self.assertEqual(self.image.A4_PORTRAIT, self.image.get_a4_dimensions())

    @patch('apps.image_services.models.ImageFile.dimensions', new_callable=mock.PropertyMock)
    def test_resize_image(self, mock_dimensions):
        mock_dimensions.return_value = (1000, 800)
        with self.assertRaises(Exception):
            self.image.resize_image()

        self.assertEqual(self.image.resize_image(new_height=796), (995, 796))


class ImageTestService(APITestCase):

    def test_image_service(self):
        url = reverse('image:image-process')
        test_data = {
            'width': 500,
            'height': 300,
            'orientation': 'Horizontal'
        }

        # create a image file to send in the request
        file = io.BytesIO()
        image = Image.new('RGBA', size=(test_data['width'], test_data['height']), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)

        response = self.client.post(url, {'file': file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, test_data)
