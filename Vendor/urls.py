from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Vendor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/$', 'vendorApp.views.articles'),
    url(r'^articles/popular/$', 'vendorApp.views.popular', name='popular'),
    url(r'^articles/tech/$', 'vendorApp.views.tech', name='popular'),
)

 	