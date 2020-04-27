from rest_framework import serializers

from portailva.association.api_v1.serializers import ShortAssociationSerializer
from portailva.event.models import Event, EventType, EventPrice
from portailva.utils.api_v1.serializers import PlaceSerializer


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EventType
        fields = ('id', 'name', 'color')


class EventPriceSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta(object):
        model = EventPrice
        fields = ('id', 'name', 'price', 'is_va', 'is_variable',)

    def get_price(self, obj):
        if obj.is_variable:
            return None
        else:
            return obj.price


class EventSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    association = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    affichage = serializers.SerializerMethodField()

    class Meta(object):
        model = Event
        fields = ('id', 'name', 'short_description', 'description', 'type', 'association', 'location', 'begins_at', 'ends_at',
                  'prices', 'website_url', 'logo_url', 'facebook_url', 'affichage')

    def get_location(self, obj):
        return PlaceSerializer(obj.place).data

    def get_type(self, obj):
        return EventTypeSerializer(obj.type).data

    def get_association(self, obj):
        return ShortAssociationSerializer(obj.association).data

    def get_prices(self, obj):
        return EventPriceSerializer(obj.prices, many=True).data

    def get_logo_url(self, obj):
        if not obj.logo_url or obj.logo_url == '':
            return obj.association.logo_url
        return obj.logo_url

    def get_affichage(self, obj):
        data = {}
        if obj.has_poster:
            data['begin_publication_at'] = obj.begin_publication_at
            data['end_publication_at'] = obj.end_publication_at
            data['content_url'] = obj.content_url
            data['duration'] = obj.duration
        return data
