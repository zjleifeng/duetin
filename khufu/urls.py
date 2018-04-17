from django.conf.urls import include, url
from django.contrib import admin
from .views import obtain_expiring_auth_token

import settings
from django.views.static import serve
from khufu.views import index, policy, permission_denied, page_error, page_not_found
# import notifications.urls
from social_core.utils import setting_name

extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''
from . import views
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

urlpatterns = [
    # Examples:
    url(r'^$', index, name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^privacypolicy/$', policy),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/account/', include('app_auth.urls')),
    url(r'^api/v1/sing/', include('khafre.sing.urls')),

    url(r'^api/v1/music/', include('khafre.main.urls')),

    url(r'^api/v1/manage/', include('khafre.manage.urls')),

    url(r'^api/v1/feed/', include('khafre.feed.urls')),

    url(r'^api/v1/notification/', include('khafre.message.urls')),

    # url(r'^api/v1/', include('khafre.music.urls')),
    # url(r'^api/v1/token/', obtain_expiring_auth_token, name='api-token'),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^media/music/(?P<path>.*)', serve,
        {'document_root': settings.MEDIA_ROOT + '/music'}),
    # url(r'^ok/complete/(?P<backend>[^/]+){0}$'.format(extra), views.complete),
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    url(r'', include('fcm.urls')),
    url(r'^operate/', include('operate.urls')),
    url('', include('social_django.urls', namespace='social'))

]
# handler403 = permission_denied
# handler404 = page_not_found
# handler500 = page_error
