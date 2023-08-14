from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializer import AccountSerializer
# Create your views here.

class AccountAPIView(APIView):
    def post(self, request):
        pass

    def get(self, request):
        pass

class AccountDetailAPIView(APIView):
    def get(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        pass