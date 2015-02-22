from rest_framework import serializers
from models import Article


class ArticleSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=True, max_length=255)
    text = serializers.CharField(required=True)
    source = serializers.CharField(required=True, max_length=255)
    coverPic = serializers.CharField(required=True, max_length=255)
    section = serializers.CharField(required=True, max_length=255)
    logo = serializers.CharField(required=True, max_length=255)
    popularity = serializers.IntegerField(default=0)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.id = attrs.get('id', instance.id)
            instance.title = attrs.get('title', instance.title)
            instance.text = attrs.get('text', instance.text)
            instance.source = attrs.get('source', instance.source)
            instance.coverPic = attrs.get('coverPic', instance.coverPic)
            instance.section = attrs.get('section', instance.section)
            instance.logo = attrs.get('logo', instance.logo)
            instance.popularity = attrs.get('popularity', instance.popularity)
            return instance

        return Article(attrs.get('id'), attrs.get('title'), attrs.get('text'), attrs.get('source'),
                       attrs.get('coverPic'), attrs.get('section'), attrs.get('logo'), attrs.get('popularity'))