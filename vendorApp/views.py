import os
import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from models import Article
from serializers import ArticleSerializer
from mongoengine import connect, DoesNotExist

TRENDING_LIMIT = 25  # number of items
TRENDING_LIFESPAN = 1  # number of days
DEFAULT_FILTERS = ['-dateAdded', 'mixIndex']
TRENDING_FILTERS = ['-popularity', 'mixIndex', '-dateAdded']

# connect to MongoDB
conn_uri = os.environ.get('MONGOLAB_URI')
DB_NAME = 'vendor'
if conn_uri is not None:  # production env
    connect(DB_NAME, host=conn_uri)
else:  # development env, using localhost
    connect(DB_NAME)


# utility sorting function
def multi_key_sort(items, columns):
    from operator import itemgetter
    comparators = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                    (itemgetter(col.strip()), 1)) for col in columns]

    def comparator(left, right):
        for fn, multiple in comparators:
            result = cmp(fn(left), fn(right))
            if result:
                return multiple * result
        else:
            return 0
    return sorted(items, cmp=comparator)


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


def get_trending_by_region(region):
    today = datetime.datetime.today()
    age = datetime.timedelta(days=TRENDING_LIFESPAN)
    time_limit = today - age
    articles = [article for article in Article.objects(region=region, dateAdded__gte=time_limit)[:TRENDING_LIMIT]]
    return multi_key_sort(articles, TRENDING_FILTERS)


def get_gossip_by_region(region):
    articles = [article for article in Article.objects(region=region, section='Gossip')]
    return multi_key_sort(articles, DEFAULT_FILTERS)


def get_tech_by_region(region):
    articles = [article for article in Article.objects(region=region, section='Tech')]
    return multi_key_sort(articles, DEFAULT_FILTERS)


def get_headlines_by_region(region):
    articles = [article for article in Article.objects(region=region, section='Headlines')]
    return multi_key_sort(articles, DEFAULT_FILTERS)


def get_business_by_region(region):
    articles = [article for article in Article.objects(region=region, section='Business')]
    return multi_key_sort(articles, DEFAULT_FILTERS)


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
