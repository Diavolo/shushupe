from uuid import uuid4
from rest_framework import serializers


class SecretKeySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    django_secret_key = serializers.CharField()
    flask_secret_key = serializers.CharField()
    secret_key = serializers.CharField()
