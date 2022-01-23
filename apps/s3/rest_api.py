from django.http import FileResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from apps.s3.models import File
from apps.s3.serializers import FileSerializer


class MospolytechUserViewSet(mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             viewsets.GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=True, methods=['GET'], url_path='download')
    def download(self, request, *args, **kwargs):
        file = self.get_object()
        return FileResponse(file.data)
