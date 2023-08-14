from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AccountAPIView, AccountDetailAPIView
urlpatterns = [
    path('write', AccountAPIView.as_view(), name='PostAccountAPIView'),
    path('', AccountAPIView.as_view(), name='GetAccountAPIView'),
    path('<int:account_id>', AccountDetailAPIView.as_view(), name='DetailAccountAPIView'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)