from django.urls import path
from .views import SignupAPIView, LoginAPIView, UserAPIView, RefreshAPIView, AdminLoginAPIView, AdminSignupAPIView, kakao_login, kakao_callback
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),                     # 회원가입
    path('login', LoginAPIView.as_view(), name='login'),                        # 로그인
    path('info', UserAPIView.as_view(), name='user-info-update'),               # 사용자 정보 수정
    path('refresh', RefreshAPIView.as_view(), name='refresh-login'),            # refresh 로그인
    path('admin-signup', AdminSignupAPIView.as_view(), name='admin-signup'),    # 관리자 계정 회원가입
    path('admin-login', AdminLoginAPIView.as_view(), name='admin-login'),       # 관리자 계정 로그인
    path('account/login/kakao/', kakao_login, name='kakao_login'),
    path('account/login/kakao/callback/', kakao_callback, name='kakao_callback'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)