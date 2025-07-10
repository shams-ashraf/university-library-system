from django.contrib import admin # type: ignore
from django.urls import include, path # type: ignore
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('library.urls')),
    path('admin/', admin.site.urls),
]