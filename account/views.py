from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from user.models import CustomAbstractBaseUser
from .serializer import AccountSerializer
from rest_framework.authentication import get_authorization_header
from user.authentication import decode_access_token
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.utils.dateformat import DateFormat
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
    
    # 장부 전체 조회 query = ?year=2023&month=08
    def get(self, request):
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        paginator = PageNumberPagination()

        # 페이지 내의 최대 객체 수 = 31 (한 달)
        paginator.page_size = 31

        # ?year=Null, 현재 년도 반환 = yyyy 포맷
        if year is None:
            year = DateFormat(datetime.now()).format('Y')

        # ?month=Null, 현재 월 반환 = mm 포맷
        if month is None:
            month = DateFormat(datetime.now()).format('m')
        
        # Account DB모델에서 year, month로 필터링
        account = Account.objects.filter(
            designate_date__year=year, 
            designate_date__month=month
            )
        result = paginator.paginate_queryset(account, request)

        try:
            serializer = AccountSerializer(result, many = True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AccountDetailAPIView(APIView):
    def get(self, request, account_id):
        try:
            account = Account.objects.get(pk = account_id)
            serializer = AccountSerializer(account, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, account_id):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            account = Account.objects.get(pk = account_id)
            # 해당 장부 작성자인지 확인
            if decode_access_token(auth[1]) == account.admin_user_id:
                serializer = AccountSerializer(account, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save(data=request.data, request=request)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'Message':'수정 권한이 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, account_id):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            account = Account.objects.get(pk = account_id)
            
            # 해당 장부 작성자인지 확인
            if decode_access_token(auth[1]) == account.admin_user_id:
                account.delete()
                return Response({'Message':'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'Message':'수정 권한이 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)