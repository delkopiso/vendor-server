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

    serializer = ArticleSerializer(article)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_popular(request):
    results = []
    for article in Article.objects(section='Popular'):
        results.append(article)
    serialized_list = ArticleSerializer(results, many=True)
    return Response(serialized_list.data)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_tech(request):
    results = []
    for article in Article.objects(section='Tech'):
        results.append(article)
    serialized_list = ArticleSerializer(results, many=True)
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
