import datetime
from rest_framework import serializers
from models import Article


class ArticleSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=True, max_length=255)
    source = serializers.CharField(required=True, max_length=255)
    coverPic = serializers.CharField(required=True, max_length=255)
    section = serializers.CharField(required=True, max_length=255)
    logo = serializers.CharField(required=True, max_length=255)
    popularity = serializers.IntegerField(default=0)
    mixIndex = serializers.IntegerField(default=0)
    dateAdded = serializers.DateTimeField(default=datetime.datetime.now())
    region = serializers.CharField(required=True, max_length=255)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.id = attrs.get('id', instance.id)
            instance.title = attrs.get('title', instance.title)
            instance.source = attrs.get('source', instance.source)
            instance.coverPic = attrs.get('coverPic', instance.coverPic)
            instance.section = attrs.get('section', instance.section)
            instance.logo = attrs.get('logo', instance.logo)
            instance.popularity = attrs.get('popularity', instance.popularity)
            instance.region = attrs.get('region', instance.region)
            return instance

        return Article(attrs.get('id'), attrs.get('title'), attrs.get('source'), attrs.get('region'),
                       attrs.get('coverPic'), attrs.get('section'), attrs.get('logo'), attrs.get('popularity'))

class LogoSerializer(serializers.Serializer):
    
    logo = serializers.CharField(required=True, max_length=255)
    
    def restore_object(self, attrs, instance=None):
        if instance:
            instance.logo = attrs.get('logo', instance.logo)
            return instance

        return Article(attrs.get('logo'))