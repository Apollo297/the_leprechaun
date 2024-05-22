from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('capital/', include('capital.urls', namespace='capital')),
    path('goals/', include('goals.urls', namespace='goals')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('main.urls', namespace='main')),
]

# urlpatterns += static(
#         settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
#     )
