import datetime
from mongoengine import Document, StringField, IntField, DateTimeField, queryset_manager


class Article(Document):
    title = StringField(required=True, max_length=255)
    source = StringField(required=True, unique=True, max_length=255)
    coverPic = StringField(required=True, max_length=255)
    section = StringField(required=True, max_length=255)
    logo = StringField(required=True, max_length=255)
    popularity = IntField(default=0)
    mixIndex = IntField(default=0)
    dateAdded = DateTimeField(default=datetime.datetime.now())

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset
