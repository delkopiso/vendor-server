import os
import datetime
import math

from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from mongoengine import connect, DoesNotExist

from models import Article

from serializers import ArticleSerializer


TRENDING_LIMIT = 30  # number of items
TRENDING_LIFESPAN = 2   # number of days
PAGE_SIZE_PARAM = 'size'
PAGE_NUMBER_PARAM = 'page'
DEFAULT_PAGE_SIZE = 5
STARTUP_PAGE_SIZE = 3
FIRST_PAGE = 1

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


def get_articles_by_region(region, limit, offset):
    base_query = Article.objects(region=region)
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size

def get_trending_by_region(region, limit, offset):
    today = datetime.datetime.today()
    age = datetime.timedelta(days=TRENDING_LIFESPAN)
    time_limit = today - age
    base_query = Article.objects(region=region, dateAdded__gte=time_limit)
    query_size = TRENDING_LIMIT
    return base_query.order_by('-popularity', 'mixIndex', '-dateAdded').skip(offset).limit(limit), query_size


def get_gossip_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Gossip')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size


def get_tech_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Tech')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size


def get_headlines_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Headlines')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size


def get_business_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Business')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size

def get_sports_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Sports')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size

def get_fashion_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Fashion')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size

def get_politics_by_region(region, limit, offset):
    base_query = Article.objects(region=region, section='Politics')
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size

def get_section_articles_by_region(region, sectionA, sectionB, sectionC, limit, offset):
    base_query = Article.objects(region=region, section__in=[sectionA, sectionB, sectionC])
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').skip(offset).limit(limit), query_size

def get_region_logos_for_section_do(region,section):
    base_query = Article.objects(region=region, section=section.capitalize()).only("logo")
    query_size = len(base_query)
    return base_query.order_by('-dateAdded', 'mixIndex').distinct("logo"), query_size


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_startup(request, region):
    current_page = int(request.GET.get(PAGE_NUMBER_PARAM, FIRST_PAGE))
    page_size = int(request.GET.get(PAGE_SIZE_PARAM, STARTUP_PAGE_SIZE))
    offset = page_size * (current_page - 1)
    trending = ArticleSerializer(get_trending_by_region(region, page_size, offset)[0], many=True).data
    gossip = ArticleSerializer(get_gossip_by_region(region, page_size, offset)[0], many=True).data
    tech = ArticleSerializer(get_tech_by_region(region, page_size, offset)[0], many=True).data
    business = ArticleSerializer(get_business_by_region(region, page_size, offset)[0], many=True).data
    headlines = ArticleSerializer(get_headlines_by_region(region, page_size, offset)[0], many=True).data
    fashion = ArticleSerializer(get_fashion_by_region(region, page_size, offset)[0], many=True).data
    sports = ArticleSerializer(get_sports_by_region(region, page_size, offset)[0], many=True).data
    politics = ArticleSerializer(get_politics_by_region(region, page_size, offset)[0], many=True).data
    content = {
        "trending": trending,
        "gossip": gossip,
        "tech": tech,
        "business": business,
        "headlines": headlines,
        "fashion": fashion,
        "sports": sports,
        "politics": politics
    }
    return Response(content)



def generate_output(query_func, region, request):
    current_page = int(request.GET.get(PAGE_NUMBER_PARAM, FIRST_PAGE))
    current_page = current_page if current_page > FIRST_PAGE else FIRST_PAGE
    page_size = int(request.GET.get(PAGE_SIZE_PARAM, DEFAULT_PAGE_SIZE))
    offset = page_size * (current_page - 1)
    results = query_func(region, page_size, offset)
    count = results[1]
    last_page = int(math.ceil(count / page_size))
    prev_page = current_page - 1 if current_page > FIRST_PAGE else None
    next_page = current_page + 1 if current_page < last_page else None

    return {
        'first_page': FIRST_PAGE,
        'previous_page': prev_page,
        'current_page': current_page,
        'next_page': next_page,
        'last_page': last_page,
        'count': count,
        'results': ArticleSerializer(results[0], many=True).data
    }

def generate_output_sectionwise(query_func, region,section, request):
    results = query_func(region, section)
    count = results[1]
    return {
        'count': count,
        'results': results[0]
    }


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_articles(request, region):
    return Response(generate_output(get_articles_by_region, region, request))

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_home(request, region):
    return Response(generate_output(get_home_articles, region, request))


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_trending(request, region):
    return Response(generate_output(get_trending_by_region, region, request))

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_gossip(request, region):
    return Response(generate_output(get_gossip_by_region, region, request))


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_tech(request, region):
    return Response(generate_output(get_tech_by_region, region, request))


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_headlines(request, region):
    return Response(generate_output(get_headlines_by_region, region, request))


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_business(request, region):
    return Response(generate_output(get_business_by_region, region, request))

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_sports(request, region):
    return Response(generate_output(get_sports_by_region, region, request))

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_fashion(request, region):
    return Response(generate_output(get_fashion_by_region, region, request))

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_politics(request, region):
    return Response(generate_output(get_politics_by_region, region, request))  

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_section_articles(request, region, sectionA, sectionB, sectionC):
    return Response(generate_output(get_section_articles_by_region, region, sectionA, sectionB, sectionC, request))  

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_region_logos_for_section(request, region, section):
    return Response(generate_output_sectionwise(get_region_logos_for_section_do, region,section, request))
  
