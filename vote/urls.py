from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import VoteAPIView, QuestionAPIView

urlpatterns = [
    path('<int:board_id>', QuestionAPIView.as_view(), name="QuestionAPI" ),
    path('<int:board_id>/<int:choice_id>', VoteAPIView.as_view(), name="VoeteAPI"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)