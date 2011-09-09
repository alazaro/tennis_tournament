from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import core.urls

handler500 = 'djangotoolbox.errorviews.server_error'

admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^', include(core.urls)),
)

urlpatterns += staticfiles_urlpatterns()
