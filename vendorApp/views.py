from django.shortcuts import render
import django_filters
from rest_framework import filters
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from pymongo import Connection, DESCENDING
from models import Article
from serializers import ArticleSerializer

@csrf_exempt
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def articles(request, format=None):
    #filter_backends = (filters.OrderingFilter,)
    #ordering_fields = ('index')
    #connect to our local mongodb
    db = Connection('localhost',27017)
    #get a connection to our database
    dbconn = db.vendor
    articleCollection = dbconn['articles']
    articles = []
    for r in articleCollection.find().sort('index', DESCENDING):
        article = Article( r["_id"] , r["title"] , r["text"] , r["source"] , r["coverPic"] , r["section"], r["logo"], r["index"])
        articles.append(article)
    serializedList = ArticleSerializer(articles, many=True)
    return Response(serializedList.data)

@csrf_exempt
@api_view(['GET'])
def popular(request):
    #connect to our local mongodb
    db = Connection('localhost',27017)
    #get a connection to our database
    dbconn = db.vendor
    articleCollection = dbconn['articles']
    articles = []
    for r in articleCollection.find({'section':'Popular'}).sort('index', DESCENDING):
        article = Article( r["_id"] , r["title"] , r["text"] , r["source"] , r["coverPic"] , r["section"], r["logo"], r["index"])
        articles.append(article)
    serializedList = ArticleSerializer(articles, many=True)
    return Response(serializedList.data)

@csrf_exempt
@api_view(['GET'])
def tech(request):
    #connect to our local mongodb
    db = Connection('localhost',27017)
    #get a connection to our database
    dbconn = db.vendor
    articleCollection = dbconn['articles']
    articles = []
    for r in articleCollection.find({'section':'Tech'}).sort('index', DESCENDING):
        article = Article( r["_id"] , r["title"] , r["text"] , r["source"] , r["coverPic"] , r["section"], r["logo"], r["index"])
        articles.append(article)
    serializedList = ArticleSerializer(articles, many=True)
    return Response(serializedList.data)


