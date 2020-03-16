from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from portailva.utils.api_v1.serializers import PlaceSerializer
from portailva.utils.models import Place


class PlaceAPIView(ListAPIView):
    serializer_class = PlaceSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Place.objects.all()
