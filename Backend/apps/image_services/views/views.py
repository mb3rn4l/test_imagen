# from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.image_services.serializers import ProcessImageSerializer


class ProcessImage(GenericAPIView):
    serializer_class = ProcessImageSerializer
    """
    Service that process an image to fit it in A4 sheet
    """
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.fit_image_in_A4_sheet()
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
