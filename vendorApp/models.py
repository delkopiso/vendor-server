import datetime
from mongoengine import Document, StringField, IntField, DateTimeField, queryset_manager


class Article(Document):
    title = StringField(required=True, max_length=255)
    text = StringField(required=True)
    source = StringField(required=True, unique=True, max_length=255)
    coverPic = StringField(required=True, max_length=255)
    section = StringField(required=True, max_length=255)
    logo = StringField(required=True, max_length=255)
    popularity = IntField(default=0)
    mixIndex = IntField(default=0)
    dateAdded = DateTimeField(default=datetime.datetime.now())

    @queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('-popularity')