from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AccountAPIView
urlpatterns = [
    path('write', AccountAPIView.as_view(), name='PostAccountAPIView'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)