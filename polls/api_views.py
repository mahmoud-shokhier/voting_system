from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import *
from .serializers import *
from voting.middleware.check_token import CheckTokenMiddleware

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

