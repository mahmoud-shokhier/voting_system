from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import *
from .serializers import *
from voting.middleware.check_token import CheckTokenMiddleware
from django.db.models import F

class PollsPagination(LimitOffsetPagination):
    default = 1
    max_limit = 10

class PollList(ListAPIView):
    authentication_classes=(CheckTokenMiddleware, )
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_fields = ('id', )
    search_fields = ('name', 'description')
    pagination_class = PollsPagination
    
    def get_queryset(self):
        """
        Optionally restricts the returned poll by order it usgin expiry date ASC.
        """
        queryset = Poll.objects.order_by('-expiry_date_time')
        return queryset

   
class PollVote(CreateAPIView):
    serializer_class = VoteSerializer
    authentication_classes=(CheckTokenMiddleware, )
    queryset = UserChoice.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            choice_id = request.data.get('choice_id')
            poll_id = request.data.get('poll_id')
            print(UserChoice.objects.filter(user=request.user, poll_id=poll_id).exists())
            if UserChoice.objects.filter(user=request.user, poll_id=poll_id).exists():
                raise serializers.ValidationError({'one_time_Vote': 'You are permitted to vote only once'})
            else:
                Choice.objects.filter(id=choice_id).update(votes=F('votes')+1)
                data = VoteSerializer(UserChoice.objects.create(user=request.user, choice_id=choice_id, poll_id=poll_id)).data
                return Response(data, status=200)
        except ValueError:
            raise ValidationError({'error': 'unexpected error occur'})

class PollComment(CreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes=(CheckTokenMiddleware, )
    queryset = Comment.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            comment = request.data.get('comment')
            poll_id = request.data.get('poll_id')
            data = CommentSerializer(Comment.objects.create(user=request.user, comment_text=comment, poll_id=poll_id)).data
            return Response(data, status=200)
        except ValueError:
            raise ValidationError({'error': 'unexpected error occur'})
