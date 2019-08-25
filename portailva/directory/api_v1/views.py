from django.http import Http404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from portailva.directory.models import DirectoryEntry
from .serializers import DirectoryEntrySerializer, PrivateDirectoryEntrySerializer, DetailDirectoryEntrySerializer


class DirectoryAPIView(ListAPIView):
    serializer_class = DirectoryEntrySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return DirectoryEntry.objects.get_last_active()


class PublicDirectoryByIdAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DetailDirectoryEntrySerializer

    def get_object(self):
        try:
            return DirectoryEntry.objects.get_last_for_association_id(self.kwargs.get('association_pk'))
        except IndexError:
            raise Http404


class PrivateDirectoryAPIView(DirectoryAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = PrivateDirectoryEntrySerializer
