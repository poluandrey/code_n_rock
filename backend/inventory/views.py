from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .models import File
from .serializers import FileUploadSerializer, FileSerializer


class FileUploadView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            files = serializer.save()
            data = {'detail': files, 'status': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        data = {"detail": serializer.errors, 'status': False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)