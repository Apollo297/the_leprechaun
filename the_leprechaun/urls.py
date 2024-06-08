from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('capital/', include('capital.urls', namespace='capital')),
    path('goals/', include('goals.urls', namespace='goals')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('main.urls', namespace='main')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
