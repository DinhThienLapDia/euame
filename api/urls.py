from django.conf.urls import re_path, include

urlpatterns = [
	re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
