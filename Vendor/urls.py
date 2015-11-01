from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Vendor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^article/(?P<article_id>[0-9a-fA-F]{24})/$', 'vendorApp.views.get_article'),
    url(r'^startup/region/(?P<region>[a-z]+)/$', 'vendorApp.views.get_region_startup', name='start_combined'),
    # url(r'^region/(?P<region>[a-z]+)/$', 'vendorApp.views.get_region_all', name='combined'),
    
    #url(r'^regions/(?P<region>[a-z]+)/home/$', 'vendorApp.views.get_region_home', name='home_articles'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/$', 'vendorApp.views.get_region_articles', name='all_articles'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/trending/$', 'vendorApp.views.get_region_trending', name='trending'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/gossip/$', 'vendorApp.views.get_region_gossip', name='gossip'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/tech/$', 'vendorApp.views.get_region_tech', name='tech'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/headlines/$', 'vendorApp.views.get_region_headlines', name='headlines'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/business/$', 'vendorApp.views.get_region_business', name='business'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/sports/$', 'vendorApp.views.get_region_sports', name='sports'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/fashion/$', 'vendorApp.views.get_region_fashion', name='fashion'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/politics/$', 'vendorApp.views.get_region_politics', name='politics'),

    url(r'^regions/(?P<region>[a-z]+)/articles/(?P<section>[a-z]+)/$', 'vendorApp.views.get_region_section'),
    url(r'^regions/(?P<region>[a-z]+)/articles/(?P<sectionA>[a-z]+)/(?P<sectionB>[a-z]+)/(?P<sectionC>[a-z]+)/$', 'vendorApp.views.get_region_section_combo'),
    url(r'^regions/(?P<region>[a-z]+)/articlelogos/(?P<section>[a-z]+)/$', 'vendorApp.views.get_region_logos_for_section'),
    #url(r'^regions/(?P<region>[a-z]+)/articles/home/(?P<sections[0]>[a-z]+)/$', 'vendorApp.views.get_region_articles_section'),
    # url(r'^article/like/(?P<article_id>[0-9a-fA-F]{24})/$', 'vendorApp.views.like_article'),
    # url(r'^article/dislike/(?P<article_id>[0-9a-fA-F]{24})/$', 'vendorApp.views.dislike_article'),
)