from django.conf.urls import re_path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
