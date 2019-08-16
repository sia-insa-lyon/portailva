from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from portailva.directory.models import DirectoryEntry
from .serializers import DirectoryEntrySerializer, PrivateDirectoryEntrySerializer


class DirectoryAPIView(ListAPIView):
    serializer_class = DirectoryEntrySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return DirectoryEntry.objects.get_last_active()


class PrivateDirectoryAPIView(DirectoryAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = PrivateDirectoryEntrySerializer
