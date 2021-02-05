from rest_framework import serializers


class ConfigureSerializer(serializers.Serializer):
    type = serializers.CharField()


class KeywordSerializer(serializers.Serializer):
    key = serializers.CharField()


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
    keyword = serializers.ListSerializer(child=KeywordSerializer(), source='get_keyword')
    configure = ConfigureSerializer(source='get_configure')


class SiteElasticsearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    og_title = serializers.CharField()
    og_description = serializers.CharField()
    keyword = serializers.ListSerializer(child=KeywordSerializer(), source='get_keyword')

