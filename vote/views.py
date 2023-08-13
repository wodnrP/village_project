from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from .models import Vote, Choice
from board.models import Board
from .serializer import VoteSerializer, ChoiceSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from user.authentication import decode_access_token
# Create your views here.

class QuestionAPIView(APIView):
    # 투표 생성
    def post(self, request, board_id):
        board = get_object_or_404(Board, pk=board_id)
        vote = Vote.objects.create(board=board, title=request.data["title"])

        # 선택지 생성
        choice_data = request.data.get('choices', [])
        if not choice_data:
            return Response({'Message': '선택지를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 요청된 투표 항목 수 만큼 choices에 담아서 저장
        choices = []
        for data in choice_data:
            choice = Choice.objects.create(content=data.get('content', ''), vote=vote)
            choices.append(choice)

        return Response({'Message': 'Success'}, status=status.HTTP_201_CREATED)

class VoteAPIView(APIView):
    # 투표 하기
    @transaction.atomic
    def post(self, request, board_id, choice_id):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            board = get_object_or_404(Board, pk=board_id)
            vote = Vote.objects.get_or_create(board=board)[0]
            choice = get_object_or_404(Choice, pk=choice_id, vote=vote)
            
            # 중복 투표 방지
            user = decode_access_token(auth[1])
            if choice.voter.filter(pk=user).exists():
                return Response({'Message': '이미 투표하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # 투표 수 증가
            choice.count += 1
            choice.voter.add(user)
            choice.save()

            return Response({'Message': 'Success'}, status=status.HTTP_201_CREATED)
            
    # 투표 조회
    def get(self, request):
        pass

    def delete(self, request, vote_id):
        pass
