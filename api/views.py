from rest_framework import viewsets, response
from api import serializers
from api.models import RandomSecretApiKey


class SecretKeyViewSet(viewsets.ViewSet):
    """Generate a set of random secret keys."""
    serializer_class = serializers.SecretKeySerializer()

    def list(self, request):
        serializer = serializers.SecretKeySerializer(RandomSecretApiKey())
        return response.Response(serializer.data)
