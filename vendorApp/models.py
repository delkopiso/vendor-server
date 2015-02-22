from mongoengine import *


class Article(Document):
    title = StringField(required=True, max_length=200)
    text = StringField(required=True, max_length=200)
    source = StringField(required=True, unique=True, max_length=200)
    coverPic = StringField(required=True, max_length=200)
    section = StringField(required=True, max_length=200)
    logo = StringField(required=True, max_length=200)
    popularity = IntField(default=0)

    @queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('-popularity')