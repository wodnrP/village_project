from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.authentication import get_authorization_header
from .authentication import create_access_token, create_refresh_token, access_token_exp, decode_access_token, decode_refresh_token
from .serializer import UserSerializer
from .models import CustomAbstractBaseUser
import hashlib
from django.shortcuts import redirect
import urllib.parse
# # Create your views here.

# 회원가입 에러 처리
class SignupException(APIException):
    status_code = 400
    default_detail = '실패! 입력한 정보를 다시 확인해주세요'
    default_code = 'KeyNotFound'

# 로그인 에러 처리 
class LoginException(APIException):
    status_code = 400
    default_detail = '아이디 혹은 비밀번호를 다시 확인해주세요'
    default_code = 'KeyNotFound'

class EmailException(APIException):
    status_code = 400
    default_detail = '올바른 이메일 형식이 아닙니다. @를 입력해주세요.'
    default_code = 'KeyNotFound'

class PasswordException(APIException):
    status_code = 400
    default_detail = '비밀번호를 8자리 이상 입력해주세요'
    default_code = 'KeyNotFound'

class TokenErrorException(APIException):
    status_code = 403
    if status_code == 403:
        status_code = 401
    default_detail = 'unauthenticated'

# 관리자 로그인 에러 처리
class AdminException(APIException):
    status_code = 400
    default_detail  = '관리자 계정이 아닙니다.'
    default_code = 'KeyNotFound'

# 로그인/회원가입시 토큰 생성 함수
def token_create(user):    
    access_token = create_access_token(user.id)
    access_exp = access_token_exp(access_token)
    refresh_token = create_refresh_token(user.id)

    response = Response(status=status.HTTP_201_CREATED)
    response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)         #리프레쉬 토큰 쿠키에 저장
    response.data = {
        'access_token' : access_token,
        'access_exp' : access_exp,
        'refresh_token' : refresh_token
    }
    return response

# 사용자 일반 회원가입 API (회원가입시 즉시 로그인)
class SignupAPIView(APIView):
    def post(self, request):
        # email 유효성 검사 : @ 포함 
        if "@" not in request.data['email']:
            raise EmailException()
        # password 유효성 검사 : 8자 이상
        if len(request.data['password']) <= 8 :
            raise PasswordException()
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = CustomAbstractBaseUser.objects.filter(email=request.data['email']).first()
            
            # 중복되는 유저가 있는지 확인
            if not user:
                raise SignupException()
            if not user.check_password(request.data['password']):
                raise SignupException()

            # 가입한 유저 토큰 생성 및 로그인
            return token_create(user)

# 사용자 일반 로그인 API
class LoginAPIView(APIView):
    def post(self, request):
        # email 유효성 검사 : @ 포함 
        if "@" not in request.data['email']:
            raise EmailException()
        # password 유효성 검사 : 8자 이상
        if len(request.data['password']) <= 8 :
            raise PasswordException()
        
        user = CustomAbstractBaseUser.objects.filter(email=request.data['email']).first()
        
        # 사용자의 회원 정보가 있는지 확인      
        if not user:
            raise LoginException()
        
        # 사용자의 패스워드가 존재하는지 확인
        if not user.check_password(request.data['password']):
            raise LoginException()
        
        return token_create(user)

# 로그아웃 API
class LogoutAPIView(APIView):
    def delete(self, _):
        response = Response(status=status.HTTP_200_OK)
        try:
            response.delete_cookie(key="refresh_token")
            response.data = {
                'Message' : 'Logout success'
            }
            return response
        except status.HTTP_400_BAD_REQUEST:
            Response({'Message':'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)

# auth token 복호화 : id return
def token_decode(auth):
    token = auth[1].decode('utf-8')
    id = decode_access_token(token)
    return id

# 사용자 정보 수정 API
class UserAPIView(APIView):

    # 유저정보 수정
    def patch(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            user = CustomAbstractBaseUser.objects.filter(pk=token_decode(auth)).first()
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise TokenErrorException()

# refresh login
class RefreshAPIView(APIView):
    def post(self, request):
        token = request.data['refresh_token']
        
        byt_token = bytes(token, 'utf-8')

        id = decode_refresh_token(byt_token)
        access_token = create_access_token(id)
        access_exp = access_token_exp(access_token)
        return Response({
            'access_token': access_token,
            'access_exp': access_exp
        })

# building_name을 hash_encoding
def generate_building_code(building_name):
    hash_text = hashlib.sha256(building_name.encode()).hexdigest()
    return hash_text[:20]

# 관리자 회원가입 API 
class AdminSignupAPIView(APIView):
    def post(self, request):
        # email 유효성 검사 : @ 포함 
        if "@" not in request.data['email']:
            raise EmailException()
        # password 유효성 검사 : 8자 이상
        if len(request.data['password']) <= 8 :
            raise PasswordException()
        
        # admin_check defalt 값을 True로 변경 -> 관리자
        if request.data['admin_check'] != 'True':
            raise AdminException()
        
        # 관리자 building_code 생성 및 저장 
        if request.data['building_name'] is not None:
            building_code = generate_building_code(request.data['building_name'])
            
            data = {
                'email':request.data['email'],
                'password':request.data['password'],
                'building_name':request.data['building_name'],
                'admin_check': request.data['admin_check'],
                'building_num':request.data['building_num'],
                'building_code': building_code
            }

        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = CustomAbstractBaseUser.objects.filter(email=request.data['email']).first()
            
            # 중복되는 유저가 있는지 확인
            if not user:
                raise SignupException()
            if not user.check_password(request.data['password']):
                raise SignupException()

            # 가입한 유저 토큰 생성 및 로그인
            return token_create(user)
        
class AdminLoginAPIView(APIView):
    def post(self, request):
        # email 유효성 검사 : @ 포함 
        if "@" not in request.data['email']:
            raise EmailException()
        # password 유효성 검사 : 8자 이상
        if len(request.data['password']) <= 8 :
            raise PasswordException()
        
        user = CustomAbstractBaseUser.objects.filter(email=request.data['email']).first()
        
        # 사용자의 회원 정보가 있는지 확인      
        if not user:
            raise LoginException()
        
        # 사용자의 패스워드가 존재하는지 확인
        if not user.check_password(request.data['password']):
            raise LoginException()
        
        # 관리자인지 확인
        if user.admin_check == False:
            raise AdminException()
        
        return token_create(user)


# KAKAO 인가 코드 받기 
import config.my_settings as my_settings
import requests

def kakao_login(request):
    app_key = my_settings.KAKAO['REST_API_KEY']
    redirect_uri = my_settings.KAKAO['MAIN_DOMAIN']+"/users/account/login/kakao/callback"
    kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    return redirect(
        f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}'
    )

def kakao_callback(request):
    # 카카오 login redirection
    data = {
        "grant_type":"authorization_code",
        "client_id":my_settings.KAKAO['REST_API_KEY'],
        "redirect_uri":my_settings.KAKAO['MAIN_DOMAIN']+"/users/account/login/kakao/callback",
        "code":request.GET['code']
    }

    # token 요청
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = requests.post(kakao_token_api, data=data).json()['access_token']
    

    # 토큰 기반 사용자 정보 반환
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    header = {"Authorization":f"Bearer {access_token}"}
    user_info = requests.get(kakao_user_api, headers=header).json()

    print(user_info["kakao_account"])
    kakao_email = user_info["kakao_account"]["email"]

    # 카카오로 로그인 > email
    # 만약 user db와 비교했을 때 email이 있다면 중복된 email입니다. -> 일반 회원가입 유도
    # 만약 관리자가 아니고 email 중복이 아니라면, 새로운 사용자로 생성 
    # 엑세스 토큰, 리프레시 토큰 반환 
    
