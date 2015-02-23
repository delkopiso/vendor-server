import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from models import Article
from serializers import ArticleSerializer
from mongoengine import connect, DoesNotExist

# connect to MongoDB
conn_uri = os.environ.get('MONGOLAB_URI')
db = 'vendor'
if conn_uri is not None:  # production env
    connect(db, host=conn_uri)
else:  # development env, using localhost
    connect(db)


# utility sorting function
def multiKeySort(items, columns):
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


# utility query function
def get_articles_section(category=None):
    results = []
    if category is None:
        for article in Article.objects:
            results.append(article)
    else:
        for article in Article.objects(section=category):
            results.append(article)
    return multiKeySort(results, ['-popularity', 'mixIndex', '-dateAdded'])


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_articles(request):
    serialized_list = ArticleSerializer(get_articles_section(), many=True)
    return Response(serialized_list.data)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArticleSerializer(article)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_popular(request):
    serialized_list = ArticleSerializer(get_articles_section(category='Popular'), many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_tech(request):
    serialized_list = ArticleSerializer(get_articles_section(category='Tech'), many=True)
    return Response(serialized_list.data)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def like_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    article.popularity += 1
    article.save()

    serializer = ArticleSerializer(article)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def dislike_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if article.popularity > 0:
        article.popularity -= 1
        article.save()

    serializer = ArticleSerializer(article)
    return Response(serializer.data)
