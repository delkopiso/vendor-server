import os
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from mongoengine import connect, DoesNotExist

from models import Article
from serializers import ArticleSerializer


STARTUP_LIMIT = 10  # number of items
TRENDING_LIMIT = 25  # number of items
TRENDING_LIFESPAN = 1  # number of days

# connect to MongoDB
conn_uri = os.environ.get('MONGOLAB_URI')
DB_NAME = 'vendor'
if conn_uri is not None:  # production env
    connect(DB_NAME, host=conn_uri)
else:  # development env, using localhost
    connect(DB_NAME)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    article.popularity += 1
    article.save()

    serializer = ArticleSerializer(article)
    return Response(serializer.data)


def get_articles_by_region(region):
    return [article for article in Article.objects(region=region)]


def get_trending_by_region(region, startup=False):
    today = datetime.datetime.today()
    age = datetime.timedelta(days=TRENDING_LIFESPAN)
    time_limit = today - age
    articles = [article for article in
                Article.objects(region=region, dateAdded__gte=time_limit).order_by('-popularity', 'mixIndex',
                                                                                   '-dateAdded')[
                :TRENDING_LIMIT]] if not startup else [article for article in Article.objects(region=region,
                                                                                              dateAdded__gte=time_limit).order_by(
        '-popularity', 'mixIndex', '-dateAdded')[:STARTUP_LIMIT]]
    return articles


def get_gossip_by_region(region, startup=False):
    articles = [article for article in Article.objects(region=region, section='Gossip').order_by('-dateAdded',
                                                                                                 'mixIndex')] if not startup else [
        article for article in
        Article.objects(region=region, section='Gossip').order_by('-dateAdded', 'mixIndex')[:STARTUP_LIMIT]]
    return articles


def get_tech_by_region(region, startup=False):
    articles = [article for article in
                Article.objects(region=region, section='Tech').order_by('-dateAdded', 'mixIndex')] if not startup else [
        article for article in
        Article.objects(region=region, section='Tech').order_by('-dateAdded', 'mixIndex')[:STARTUP_LIMIT]]
    return articles


def get_headlines_by_region(region, startup=False):
    articles = [article for article in Article.objects(region=region, section='Headlines').order_by('-dateAdded',
                                                                                                    'mixIndex')] if not startup else [
        article for article in
        Article.objects(region=region, section='Headlines').order_by('-dateAdded', 'mixIndex')[:STARTUP_LIMIT]]
    return articles


def get_business_by_region(region, startup=False):
    articles = [article for article in Article.objects(region=region, section='Business')
        .order_by('-dateAdded', 'mixIndex')] if not startup else [article for article in
                                                                  Article.objects(region=region, section='Business')
                                                                      .order_by('-dateAdded', 'mixIndex')[
                                                                  :STARTUP_LIMIT]]
    return articles


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_all(request, region):
    content = {
        "trending": ArticleSerializer(get_trending_by_region(region), many=True).data,
        "gossip": ArticleSerializer(get_gossip_by_region(region), many=True).data,
        "tech": ArticleSerializer(get_tech_by_region(region), many=True).data,
        "business": ArticleSerializer(get_business_by_region(region), many=True).data,
        "headlines": ArticleSerializer(get_headlines_by_region(region), many=True).data
    }
    return Response(content)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_startup(request, region):
    content = {
        "trending": ArticleSerializer(get_trending_by_region(region, startup=True), many=True).data,
        "gossip": ArticleSerializer(get_gossip_by_region(region, startup=True), many=True).data,
        "tech": ArticleSerializer(get_tech_by_region(region, startup=True), many=True).data,
        "business": ArticleSerializer(get_business_by_region(region, startup=True), many=True).data,
        "headlines": ArticleSerializer(get_headlines_by_region(region, startup=True), many=True).data
    }
    return Response(content)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_articles(request, region):
    serialized_list = ArticleSerializer(get_articles_by_region(region), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_trending(request, region):
    serialized_list = ArticleSerializer(get_trending_by_region(region), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_gossip(request, region):
    serialized_list = ArticleSerializer(get_gossip_by_region(region), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_tech(request, region):
    serialized_list = ArticleSerializer(get_tech_by_region(region), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_headlines(request, region):
    serialized_list = ArticleSerializer(get_headlines_by_region(region), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_business(request, region):
    serialized_list = ArticleSerializer(get_business_by_region(region), many=True)
    return Response(serialized_list.data)
