import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from models import Article
from serializers import ArticleSerializer
from mongoengine import connect

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
def articles(request):
    results = []
    for article in Article.objects:
        results.append(article)
    serialized_list = ArticleSerializer(results, many=True)
    return Response(serialized_list.data)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def popular(request):
    results = []
    for article in Article.objects(section='Popular'):
        results.append(article)
    serialized_list = ArticleSerializer(results, many=True)
    return Response(serialized_list.data)


@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def tech(request):
    results = []
    for article in Article.objects(section='Tech'):
        results.append(article)
    serialized_list = ArticleSerializer(results, many=True)
    return Response(serialized_list.data)