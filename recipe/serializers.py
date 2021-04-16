from rest_framework import serializers, viewsets

viewsets.GenericViewSet

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = 'id', 'creator'