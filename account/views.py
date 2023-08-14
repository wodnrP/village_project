from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from user.models import CustomAbstractBaseUser
from .serializer import AccountSerializer
from rest_framework.authentication import get_authorization_header
from user.authentication import decode_access_token
# Create your views here.

class AccountAPIView(APIView):
    # 장부 작성
    def post(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            user = CustomAbstractBaseUser.objects.filter(id=decode_access_token(auth[1]))
            
            # 관리자 권한 검사 
            if user.values('admin_check')[0].get('admin_check') == True:
                serializer = AccountSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # 관리자 권한이 없을 경우
            return Response({'Message':'관리자 권한이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    # 장부 조회
    def get(self, request):
        pass    

class AccountDetailAPIView(APIView):
    def get(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        pass