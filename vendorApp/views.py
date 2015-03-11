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
def get_articles(request):
    results = []
    for article in Article.objects:
        results.append(article)
    serialized_list = ArticleSerializer(results, many=True)
    return Response(serialized_list.data)


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


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_trending(request):
    results = []
    today = datetime.datetime.today()
    age = datetime.timedelta(days=TRENDING_LIFESPAN)
    time_limit = today - age
    for article in Article.objects(dateAdded__gte=time_limit)[:TRENDING_LIMIT]:
        results.append(article)
    serialized_list = ArticleSerializer(multi_key_sort(results, TRENDING_FILTERS), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_gossip(request):
    results = []
    for article in Article.objects(section='Gossip'):
        results.append(article)
    serialized_list = ArticleSerializer(multi_key_sort(results, DEFAULT_FILTERS), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_tech(request):
    results = []
    for article in Article.objects(section='Tech'):
        results.append(article)
    serialized_list = ArticleSerializer(multi_key_sort(results, DEFAULT_FILTERS), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_headlines(request):
    results = []
    for article in Article.objects(section='Headlines'):
        results.append(article)
    serialized_list = ArticleSerializer(multi_key_sort(results, DEFAULT_FILTERS), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_business(request):
    results = []
    for article in Article.objects(section='Business'):
        results.append(article)
    serialized_list = ArticleSerializer(multi_key_sort(results, DEFAULT_FILTERS), many=True)
    return Response(serialized_list.data)
