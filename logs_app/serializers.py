from rest_framework import serializers

class LogSerializer(serializers.Serializer):
    message = serializers.CharField()
    source = serializers.CharField(required=False, allow_blank=True)
