from rest_framework import serializers


class SiteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    og_url = serializers.CharField()
    og_title = serializers.CharField()
    og_description = serializers.CharField()
    og_type = serializers.CharField()
    og_image = serializers.CharField()
    date = serializers.CharField()
