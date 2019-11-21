from rest_framework import serializers

from portailva.association.models import Association, Category


class ShortAssociationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Association
        fields = ('id', 'name', 'acronym')


class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category
        fields = ('id', 'name',)
