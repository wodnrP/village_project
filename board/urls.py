from django.urls import path
from .views import BoardAPIView, BoardDetailAPIView, CommentAPIView, CommentDelAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BoardAPIView.as_view(), name="PostBoardAPI"),
    path('<int:board_id>', BoardDetailAPIView.as_view(), name="GetUpdateDeleteBoardAPI"),
    path('', BoardAPIView.as_view(), name="GetAllBoardAPI"),
    path('comments', CommentAPIView.as_view(), name="CommentPost"),
    path('comments/<int:board_id>', CommentAPIView.as_view(), name="CommentGet"),
    path('comments/<int:comment_id>/', CommentDelAPIView.as_view(), name="CommentDelete")
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)