from django.utils import formats
from rest_framework import serializers

from portailva.association.api_v1.serializers import CategorySerializer
from portailva.directory.models import OpeningHour, DirectoryEntry
from portailva.event.api_v1.serializers import EventPriceSerializer
from portailva.event.models import Event
from portailva.utils.api_v1.serializers import PlaceSerializer


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = OpeningHour
        fields = ('day', 'begins_at', 'ends_at',)


class DetailEventsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    begins_at = serializers.SerializerMethodField()
    ends_at = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()

    class Meta(object):
        model = Event
        fields = ('id', 'name', 'type', 'begins_at', 'description', 'ends_at', 'place',
                  'prices', 'website_url', 'facebook_url', 'logo_url')

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_type(self, obj):
        return str(obj.type)

    def get_begins_at(self, obj):
        return formats.date_format(obj.begins_at, 'DATETIME_FORMAT')

    def get_ends_at(self, obj):
        return formats.date_format(obj.ends_at, 'DATETIME_FORMAT')

    def get_place(self, obj):
        return PlaceSerializer(obj.place).data

    def get_prices(self, obj):
        return EventPriceSerializer(obj.prices, many=True).data


class DirectoryEntrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    acronym = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta(object):
        model = DirectoryEntry
        fields = ['id', 'name', 'short_description', 'description', 'category', 'phone', 'website_url',
                  'facebook_url', 'twitter_url', 'instagram_url', 'acronym', 'logo_url', 'location', 'schedule',
                    'is_active']

    def get_id(self, obj):
        return obj.association_id

    def get_name(self, obj):
        return obj.association.name

    def get_category(self, obj):
        return CategorySerializer(obj.association.category).data

    def get_short_description(self, obj):
        if len(obj.description) > 150:
            return obj.description[:150] + "..."
        else:
            return obj.description

    def get_location(self, obj):
        return PlaceSerializer(obj.place).data

    def get_phone(self, obj):
        return obj.api_phone

    def get_schedule(self, obj):
        return OpeningHourSerializer(obj.opening_hours.all(), many=True).data

    def get_acronym(self, obj):
        return obj.association.acronym

    def get_logo_url(self, obj):
        return obj.association.logo_url

    def get_is_active(self, obj):
        return obj.association.is_active


class DetailDirectoryEntrySerializer(DirectoryEntrySerializer):
    public_phone = serializers.SerializerMethodField()
    opening_hours = serializers.SerializerMethodField()
    related_events = serializers.SerializerMethodField()

    class Meta(DirectoryEntrySerializer.Meta):
        model = DirectoryEntry
        fields = ['id', 'name', 'acronym', 'logo_url', 'category',
                  'description', 'public_phone', 'contact_address', 'location', 'opening_hours',
                  'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'related_events',
                    'is_active']

    def get_logo_url(self, obj):
        return obj.association.logo_url

    def get_public_phone(self, obj):
        return obj.public_phone

    def get_opening_hours(self, obj):
        return OpeningHourSerializer(obj.opening_hours.all(), many=True).data

    def get_related_events(self, obj):
        return DetailEventsSerializer(obj.association.online_events(), many=True).data


class PrivateDirectoryEntrySerializer(DirectoryEntrySerializer):
    acronym = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    is_validated = serializers.SerializerMethodField()

    class Meta(DirectoryEntrySerializer.Meta):
        fields = DirectoryEntrySerializer.Meta.fields + [
            'acronym',
            'contact_address',
            'logo_url',
            'category',
            'is_validated',
            'is_active',
        ]

    def get_acronym(self, obj):
        return obj.association.acronym

    def get_logo_url(self, obj):
        return obj.association.logo_url

    def get_category(self, obj):
        return CategorySerializer(obj.association.category).data

    def get_is_validated(self, obj):
        return obj.association.is_validated

    def get_is_active(self, obj):
        return obj.association.is_active
