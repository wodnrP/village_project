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
    def get(self, request, board_id):
        try:
            # 각 테이블 조회 
            board = get_object_or_404(Board, pk=board_id)
            vote = get_object_or_404(Vote, board=board)
            choice = Choice.objects.filter(vote=vote)

            # json 직렬화
            vote_serializer = VoteSerializer(vote)
            choice_serializer = ChoiceSerializer(choice, many=True)

            # 여러 개의 투표 항목을 담을 list 생성
            Choice_list=[]

            # 여러 투표 항목 dict를 생성 후 list에 저장
            for choice_data in choice_serializer.data:
                Choice_dict = {
                    'id':choice_data['id'],
                    'count':choice_data['count'],
                    'content':choice_data['content'],
                    'vote':choice_data['vote'],
                    'voter':choice_data['voter']
                }
                Choice_list.append(Choice_dict)

            # json 결과 값 생성
            serializer = {
                'Vote':{
                    'id':vote_serializer.data['id'],
                    'board':vote_serializer.data['board'],
                    'title':vote_serializer.data['title'],
                    'create_time':vote_serializer.data['create_time']
                },
                'Choice':Choice_list
        }
            return Response(serializer, status=status.HTTP_200_OK)
        
        except Vote.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 투표 삭제 
    def delete(self, request, vote_id):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            vote = Vote.objects.get(pk = vote_id)
            # 투표를 생성한 게시글 id 기준 게시글 필터링
            board = Board.objects.filter(pk=vote.board_id)

            # 현재 로그인 한 사용자의 id값과 게시글을 작성한 사용자의 id값 비교
            # 쿼리dict에서 키 값으로 추출 한 후 get 메서드로 값 추출 
            if decode_access_token(auth[1]) == board.values('user')[0].get('user'):
                vote.delete()
                return Response({'Message':'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'Message':'해당 게시글 작성자가 아닙니다.'}, status=status.HTTP_401_UNAUTHORIZED)
