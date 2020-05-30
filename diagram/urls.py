from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include('diagram.api.urls')),
    path('', include('diagram.pages.urls')),
    path('words/', include('diagram.words.urls')),
    path('auth/', include('diagram.person.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
