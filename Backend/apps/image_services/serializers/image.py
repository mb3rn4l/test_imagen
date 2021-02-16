from rest_framework import serializers
from apps.image_services.models import ImageFile
from PIL import Image


class ProcessImageSerializer(serializers.ModelSerializer):

    def fit_image_in_A4_sheet(self):
        try:
            image = ImageFile(file=Image.open(self.validated_data.get('file')))
            orientation = 'Vertical' if image.is_portrait() else 'Horizontal'
            (width, height) = image.process_image()
            data = {
                'width': width,
                'height': height,
                'orientation': orientation
            }

            return data

        except Exception as e:
            raise serializers.ValidationError({'file': 'Error al procesar la imagen: {}'.format(str(e))})

    class Meta:
        model = ImageFile
        fields = ('file', )
