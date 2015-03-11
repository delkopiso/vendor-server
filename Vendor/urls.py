from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Vendor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/$', 'vendorApp.views.get_articles'),
    url(r'^article/(?P<article_id>[0-9a-fA-F]{24})/$', 'vendorApp.views.get_article'),
    url(r'^articles/trending/$', 'vendorApp.views.get_trending', name='trending'),
    url(r'^articles/gossip/$', 'vendorApp.views.get_gossip', name='gossip'),
    url(r'^articles/tech/$', 'vendorApp.views.get_tech', name='tech'),
    url(r'^articles/headlines/$', 'vendorApp.views.get_headlines', name='headlines'),
    url(r'^articles/business/$', 'vendorApp.views.get_business', name='business'),
    # url(r'^article/like/(?P<article_id>[0-9a-fA-F]{24})/$', 'vendorApp.views.like_article'),
    # url(r'^article/dislike/(?P<article_id>[0-9a-fA-F]{24})/$', 'vendorApp.views.dislike_article'),
)