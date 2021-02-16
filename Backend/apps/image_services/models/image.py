from django.db import models


class ImageFile(models.Model):
    A4_PORTRAIT = (796, 1123)
    A4_LANDSCAPE = (1123, 796)

    file = models.ImageField(null=False, blank=False, verbose_name="Image", upload_to='Images')

    @property
    def dimensions(self):
        return self.file.size

    def is_portrait(self):
        (width, height) = self.dimensions
        ratio = width / float(height)

        if ratio <= 1:
            return True

        return False

    def get_a4_dimensions(self):
        a4_dimensions = self.A4_LANDSCAPE
        is_portrait = self.is_portrait()

        if is_portrait:
            a4_dimensions = self.A4_PORTRAIT

        return a4_dimensions

    def process_image(self):

        (image_width, image_height) = self.dimensions
        new_dimensions = None
        a4_dimensions = self.get_a4_dimensions()

        if image_width <= a4_dimensions[0] and image_height <= a4_dimensions[1]:
            new_dimensions = (image_width, image_height)

        if image_width > a4_dimensions[0] and image_height > a4_dimensions[1]:
            new_dimensions = self.resize_image(a4_dimensions[0], None)

            image_width = new_dimensions[0]
            image_height = new_dimensions[1]

        if image_width > a4_dimensions[0]:
            new_dimensions = self.resize_image(min(a4_dimensions[0], image_width), None)

        if image_height > a4_dimensions[1]:
            new_dimensions = self.resize_image(None, min(a4_dimensions[1], image_height))

        return new_dimensions

    def resize_image(self, new_width=None, new_height=None):
        new_dimensions = None
        (image_width, image_height) = self.dimensions

        if new_width is None and new_height is None:
            raise Exception('Indique al menos un valor de ancho o alto para redimensionar')

        # calculate the ratio of the height/width and construct the dimensions
        if new_width is None:
            ratio = new_height / float(image_height)
            new_dimensions = (int(image_width * ratio), new_height)
        else:
            ratio = new_width / float(image_width)
            new_dimensions = (new_width, int(image_height * ratio))

        return new_dimensions
